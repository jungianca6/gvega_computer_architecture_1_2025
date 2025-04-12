;Interpolacion Bilineal en x86
;Cuadrante de 100x100-->400x400

section .data
    in_file      db "cuadrante.img", 0
    out_file     db "output.img", 0
    error_msg   db "File operation failed", 10, 0
    size_error  db "Input file size incorrect", 10, 0
    
    
 ; Tamaños para imagen de entrada 100x100 y salida 400x400
    IN_IMG       equ 10000    
    OUT_IMG      equ 160000   
    
    WIDTH        equ 100      ; Ancho de la imagen de entrada
    OUT_WIDTH    equ 400      ; Ancho de la imagen de salida
    SCALE_FACTOR equ 4       ; Factor de escala (4x)

section .bss
    inputBuffer   resb IN_IMG     ; Buffer para la imagen de entrada
    outputBuffer  resb OUT_IMG    ; Buffer para la imagen de salida
    fd_in       resq 1           ; File descriptor de entrada
    fd_out      resq 1           ; File descriptor de salida

section .text
global _start

_start:
    call read_infile        ; Leer la imagen de entrada
    call interpolation      ; Aplicar interpolación bilineal
    call write_output       ; Escribir resultado
    jmp exit_success        ; Salir con éxito

; ===================================
; Abrir y leer el archivo de entrada 
; ===================================
read_infile:
    ; Abrir archivo
    mov rax, 2               ; sys_open
    lea rdi, [in_file]       ; nombre del archivo
    xor rsi, rsi             ; modo: O_RDONLY
    syscall
    mov [fd_in], rax         ; guardar file descriptor
    cmp rax, 0               ; verificar error
    jl error_exit

    ; Leer contenido
    mov rax, 0               ; sys_read
    mov rdi, [fd_in]         
    lea rsi, [inputBuffer]   ; buffer de destino
    mov rdx, IN_IMG          ; bytes a leer
    syscall
    cmp rax, IN_IMG          ; verificar tamaño
    jne size_error_exit

    ; Cerrar archivo
    mov rax, 3               ; sys_close
    mov rdi, [fd_in]
    syscall
    ret

; ==============================================
; Interpolación Bilineal (100x100 -> 400x400)
; ==============================================
interpolation:
    ; Fase 1: Calcular píxeles horizontales y verticales
    xor r12, r12             ; y original [0, 99] (filas)
.outer_loop:
    cmp r12, WIDTH
    jge .phase2              ; Fase 2
    xor r13, r13             ; x original [0, 99] (columnas)
.inner_loop:
    cmp r13, WIDTH
    jge .nextRow

    ; Calcular posición en la salida 
    ; Índice base del píxel ampliado (y*4)*400 + x*4
    
    mov rax, r12
    shl rax, 2               ; y*4
    imul rax, OUT_WIDTH      ; (y*4)*400
    mov rdx, r13
    shl rdx, 2               ; x*4
    add rax, rdx             ; Índice base = (y*4)*400 + x*4
    mov r15, rax             ; Guardar índice base

    ; Obtener píxeles originales 
    
    ; P00 = pixel original (x, y)
    mov rax, r12
    imul rax, WIDTH
    add rax, r13
    movzx rbx, byte [inputBuffer + rax]  ; P00 (x,y)


    ; P10 = (x+1, y) o copia de P00 si es borde
    cmp r13, WIDTH-1
    je .p10_edge
    movzx rcx, byte [inputBuffer + rax + 1] 
    jmp .get_p01 
.p10_edge:
    mov rcx, rbx             ;replicar P00

; P01 = (x, y+1) o copia de P00 si es borde inferior
.get_p01:
    cmp r12, WIDTH-1
    je .p01_edge
    movzx r8, byte [inputBuffer + rax + WIDTH] 
    jmp .get_p11
.p01_edge:
    mov r8, rbx             ;replicar P01 

;P11 = (x+1, y+1) o copia de P01 si es borde
.get_p11:
    cmp r13, WIDTH-1
    je .p11_edge
    cmp r12, WIDTH-1
    je .p11_edge
    movzx r9, byte [inputBuffer + rax + WIDTH + 1] ; P11 (x+1,y+1)
    jmp .edge_interpolation
.p11_edge:
    mov r9, r8               ; replicar P01

.edge_interpolation:
    ; === Interpolación horizontal: a1, a2, a3 ===
    ; Píxel a (1/4): (3/4)*P00 + (1/4)*P10
    mov rax, rbx
    imul rax, 3
    add rax, rcx             ; 3*P00 + 1*P10
    shr rax, 2               ; /4
    mov [outputBuffer + r15 + 1], al ; Escribir a1

    ; Píxel a (2/4): (2/4)*P00 + (2/4)*P10
    mov rax, rbx
    add rax, rcx             ; 1*P00 + 1*P10
    shr rax, 1               ; /2
    mov [outputBuffer + r15 + 2], al ; Escribir a2

    ; Píxel a (3/4): (1/4)*P00 + (3/4)*P10
    mov rax, rbx
    mov rdx, rcx
    imul rdx, 3
    add rax, rdx             ; 1*P00 + 3*P10
    shr rax, 2               ; /4
    mov [outputBuffer + r15 + 3], al ; Escribir a3

    ; === Interpolación vertical: c1,c2,c3 ===
    ; Píxel c (1/4): (3/4)*P00 + (1/4)*P01
    mov rax, rbx
    imul rax, 3
    add rax, r8              ; 3*P00 + 1*P01
    shr rax, 2               ; /4
    mov [outputBuffer + r15 + OUT_WIDTH], al ; Escribir c1

    ; Píxel c (2/4): (2/4)*P00 + (2/4)*P01
    mov rax, rbx
    add rax, r8              ; 1*P00 + 1*P01
    shr rax, 1               ; /2
    mov [outputBuffer + r15 + OUT_WIDTH*2], al ; Escribir c2

    ; Píxel c (3/4): (1/4)*P00 + (3/4)*P01
    mov rax, rbx
    mov rdx, r8
    imul rdx, 3
    add rax, rdx             ; 1*P00 + 3*P01
    shr rax, 2               ; /4
    mov [outputBuffer + r15 + OUT_WIDTH*3], al ; Escribir c3

    ; Pixeles originales (esquinas conocidas)
    mov [outputBuffer + r15], bl               ; P00 (x,y)
    mov [outputBuffer + r15 + SCALE_FACTOR-1], cl ; P10 (x+3,y)
    mov [outputBuffer + r15 + OUT_WIDTH*(SCALE_FACTOR-1)], r8b ; P01 (x,y+3)
    mov [outputBuffer + r15 + OUT_WIDTH*(SCALE_FACTOR-1) + SCALE_FACTOR-1], r9b ; P11 (x+3,y+3)

    ; Continuar con el siguiente píxel
    inc r13
    jmp .inner_loop

.nextRow:
    inc r12
    jmp .outer_loop

.phase2:
    ; Fase 2: Pixeles intermedios interiores
    xor r12, r12             ; y in [0,396]
.phase2_y_loop:
    cmp r12, OUT_WIDTH-SCALE_FACTOR
    jge .end_interpolation
    xor r13, r13             ; x in [0,396]
.phase2_x_loop:
    cmp r13, OUT_WIDTH-SCALE_FACTOR
    jge .phase2_nextRow

    ; Calcular índice base de bloque 4x4
    mov rax, r12
    imul rax, OUT_WIDTH
    add rax, r13
    mov r15, rax             ; Guardar índice base

    ; Obtener y leer 4 esquinas existentes del bloque
    movzx rbx, byte [outputBuffer + r15]                      ; P00
    movzx rcx, byte [outputBuffer + r15 + SCALE_FACTOR-1]     ; P10
    movzx r8, byte [outputBuffer + r15 + OUT_WIDTH*(SCALE_FACTOR-1)] ; P01
    movzx r9, byte [outputBuffer + r15 + OUT_WIDTH*(SCALE_FACTOR-1) + SCALE_FACTOR-1] ; P11

    ; === Interpolación de píxeles centrales ===
    ; Para cada fila intermedia (1, 2, 3)
    mov r14, 1               ; fila intermedia (1-3)
.inter_rows:
    cmp r14, SCALE_FACTOR-1
    jg .inter_cols

    ; Calcular pesos verticales
    mov rax, SCALE_FACTOR
    sub rax, r14             ; peso para arriba (4-1=3, 4-2=2, 4-3=1)
    mov r10, rax
    mov r11, r14             ; peso para abajo (1, 2, 3)

    ; Para cada columna intermedia (1, 2, 3)
    mov rdi, 1               ; columna intermedia (1-3)
.inter_cols_inner:
    cmp rdi, SCALE_FACTOR-1
    jg .next_inter_row

    ; Calcular pesos horizontales
    mov rax, SCALE_FACTOR
    sub rax, rdi             ; peso para izquierda (4-1=3, 4-2=2, 4-3=1)
    mov rsi, rax
    mov rdx, rdi             ; peso para derecha (1, 2, 3)

    ; Obtener píxeles horizontales superiores e inferiores
    movzx rax, byte [outputBuffer + r15 + rdi]                     ; superior
    movzx rbx, byte [outputBuffer + r15 + OUT_WIDTH*(SCALE_FACTOR-1) + rdi] ; inferior

    ; Interpolar verticalmente
    imul rax, r10            ; superior * peso arriba
    imul rbx, r11            ; inferior * peso abajo
    add rax, rbx             ; suma ponderada
    mov rbx, SCALE_FACTOR
    xor rdx, rdx
    div rbx                  ; dividir por SCALE_FACTOR

    ; Escribir píxel interpolado
    mov rbx, r14
    imul rbx, OUT_WIDTH
    add rbx, r15
    add rbx, rdi
    mov [outputBuffer + rbx], al

    inc rdi
    jmp .inter_cols_inner

.next_inter_row:
    inc r14
    jmp .inter_rows

.inter_cols:
    add r13, SCALE_FACTOR
    jmp .phase2_x_loop

.phase2_nextRow:
    add r12, SCALE_FACTOR
    jmp .phase2_y_loop

.end_interpolation:
    ret

; ================================================
; Escribir el resultado de la imagen interpolada
; ================================================
write_output:
    ; Crear/abrir archivo de salida
    mov rax, 2               ; sys_open
    lea rdi, [out_file]   ; nombre del archivo
    mov rsi, 577             ; O_WRONLY | O_CREAT | O_TRUNC
    mov rdx, 0666o           ; permisos
    syscall
    mov [fd_out], rax        ; guardar file descriptor
    cmp rax, 0               ; verificar error
    jl error_exit

    ; Escribir datos
    mov rax, 1               ; sys_write
    mov rdi, [fd_out]        
    lea rsi, [outputBuffer]    
    mov rdx, OUT_IMG        ; bytes a escribir
    syscall
    cmp rax, OUT_IMG        ; verificar escritura completa
    jne error_exit

    ; Cerrar archivo
    mov rax, 3               ; sys_close
    mov rdi, [fd_out]
    syscall
    ret

; ==============================================
; Manejo de errores
; ==============================================
error_exit:
    mov rax, 1               ; sys_write
    mov rdi, 1               ; stdout
    lea rsi, [error_msg]     ; mensaje
    mov rdx, 24              ; longitud
    syscall
    jmp exit_failure

size_error_exit:
    mov rax, 1
    mov rdi, 1
    lea rsi, [size_error]
    mov rdx, 30
    syscall
    jmp exit_failure

exit_success:
    mov rax, 60              ; sys_exit
    xor rdi, rdi             ; código 0
    syscall

exit_failure:
    mov rax, 60              ; sys_exit
    mov rdi, 1               ; código 1
    syscall

