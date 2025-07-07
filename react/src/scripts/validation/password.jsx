import * as yup from 'yup';

export const passwordValidator = yup
    .string()
    .required('Пароль обязателен')
    .min(6, 'Пароль должен быть длиной от 6 до 31 символов')
    .max(31, 'Пароль должен быть длиной от 6 до 31 символов')
    .matches(/^[A-Za-z\d@$!%*?&]+$/, 'Пароль должен содержать только латинские буквы, цифры и специальные символы')
    .matches(/(?=.*[0-9])|(?=.*[@$!%*?&])/, 'Пароль должен содержать хотя бы одну цифру или специальный символ')

export const confirmPasswordValidator = yup
    .string()
    .oneOf([yup.ref('password'), null], 'Пароли должны совпадать')