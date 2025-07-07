import {useForm} from 'react-hook-form';
import React, { useState} from 'react';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { Popup } from '../../../scripts/popup';

const schema = yup.object().shape({
    email: yup
    .string()
    .required('Почта обязательна')
    .email('Неверный формат электронной почты')
});

function FormForgotPassword(){
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const [message, setMessage] = useState('');
    const apiUrl = process.env.REACT_APP_API_URL;
    const [serverError, setServerError] = useState('');

    const {
        register,
        reset,
        formState: { errors },
        handleSubmit,
    } = useForm({
        resolver: yupResolver(schema),
    });

    const onSubmit = async (data) => {
        setServerError('');
        fetch(`${apiUrl}/auth/forgot-password`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        }).then(response => {
            if(response.ok){
                setIsPopupOpen(true);
                setMessage('Проверьте почту!');
            }
            else if(response.status===404){
                setServerError('Пользователя с данной почтой не зарегистрованно');
            }
          })
        .catch (error => {
          
        })
    }
    const handleClose = () => {
        setIsPopupOpen(false);
    };

    return (
        <section className="container-forgot-password">
            <form className="form-container" action="#" method="POST" onSubmit={handleSubmit(onSubmit)}>
                {isPopupOpen && <Popup isOpen={isPopupOpen} message={message} onClose={handleClose} urlNavigate='/' />}
                <h2>Восстановление пароля</h2>
                <div className='form-container-brim'>
                    <label for="email">Email</label>
                    <input {...register("email")} onChange={(e)=> setServerError('')} type="email" id="email" name="email" />
                    {errors.email && <p className='form-validation' style={{ color: 'red' }}>{errors.email.message}</p>}
                    {serverError && <p style={{ color: 'red' }}>{serverError}</p>}
                </div>
                <button className='submit-form' type="submit">Восстановить пароль</button>
            </form>
        </section>
    );
}

export default FormForgotPassword;