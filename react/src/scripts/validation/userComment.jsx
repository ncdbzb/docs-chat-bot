import * as yup from 'yup';

export const userCommentValidator = yup
    .string()
    .max(300, 'Комментарий должен быть не длинее 300 символов')