import * as yup from 'yup';

export const nameValidator = yup
    .string()
    .required('Имя обязательно')
    .max(31, 'Имя должно быть длиной до 31 символов')
    .matches(/^[A-Za-zА-Яа-яёЁ]+$/, 'Имя должно содержать только латинские или кириллические буквы')