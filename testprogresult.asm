
dispstr macro msg
mov dx, offset msg
mov ah,09h
int 21h
endm

.model small
.data

str1 db 100,?,100 dup('$')
str2 db 100,?,100 dup('$')

msg1 db 10,13,"enter the string1$"
msg2 db 10,13,"enter the string2$"
msg3 db 10,13,"strings are equal$"
msg4 db 10,13,"strings are not equal$"
msg5 db 10,13,"length of string1"
len1 db "$$$"
msg6 db 10,13,"length of string2"
len2 db "$$$"

.code
mov ax,@data
mov ds,ax
mov es,ax


mov dx, offset msg1
mov ah,09h
int 21h

lea dx,str1
mov ah,0ah
int 21h


mov dx, offset msg2
mov ah,09h
int 21h

lea dx,str2
mov ah,0ah
int 21h

mov al,str1+1
cmp al,str2+1
jne notequal

lea si,str1
lea di,str2
mov ch,00
mov cl,str1+1
repe cmpsb
jne notequal
dispstr  msg3
jmp exit

notequal:

mov dx, offset msg4
mov ah,09h
int 21h

exit:
mov al,str1+1
aam
add ax,3030h
mov len1,ah
mov len1+1,al

mov dx, offset msg5
mov ah,09h
int 21h


mov al,str2+1
aam
add ax,3030h
mov len2,ah
mov len2+1,al

mov dx, offset msg6
mov ah,09h
int 21h


mov ah,4ch
int 21h

end
