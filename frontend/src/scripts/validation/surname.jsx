import * as yup from 'yup';

export const surnameValidator = yup
    .string()
    .required('Фамилия обязательна')
    .max(31, 'Фамилия должна быть длиной до 31 символов')
    .matches(/^[A-Za-zА-Яа-яёЁ]+$/, 'Фамилия должна содержать только латинские или кириллические буквы')