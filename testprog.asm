
DISPSTR MACRO MSG
       MOV DX, OFFSET MSG
       MOV AH,09H
       INT 21H
  ENDM

.MODEL SMALL
.DATA

STR1 DB 100,?,100 DUP('$')
STR2 DB 100,?,100 DUP('$')

MSG1 DB 10,13,"Enter the string1$"
MSG2 DB 10,13,"Enter the string2$"
MSG3 DB 10,13,"strings are equal$"
MSG4 DB 10,13,"strings are not equal$"
MSG5 DB 10,13,"length of string1"
len1 db "$$$"
MSG6 DB 10,13,"length of string2"
len2 db "$$$"

.code
    mov ax,@data
    mov ds,ax
    mov es,ax

    dispstr msg1
    lea DX,str1
    mov ah,0Ah
    INT 21H

    dispstr msg2
    lea DX,str2
    mov ah,0Ah
    INT 21H

    MOV AL,STR1+1
    CMP AL,STR2+1
    JNE NOTEQUAL

    LEA SI,STR1
    LEA DI,STR2
    MOV CH,00
    MOV CL,STR1+1
    REPE CMPSB
    JNE NOTEQUAL
    DISPSTR  MSG3
    JMP EXIT

NOTEQUAL: DISPSTR MSG4
EXIT : MOV AL,STR1+1
       AAM
       ADD AX,3030H
       MOV LEN1,AH
       MOV LEN1+1,AL
       DISPSTR MSG5 

       MOV AL,STR2+1
       AAM
       ADD AX,3030H
       MOV LEN2,AH
       MOV LEN2+1,AL
       DISPSTR MSG6

       MOV AH,4CH
       INT 21H

END