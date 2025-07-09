import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import '../../authorization/formLogIn/formLogIn.css';
import btnPass from '../../../img/icons/password/Visibility=True.svg';
import btnPassVisib from '../../../img/icons/password/Visibility=False.svg';
import { surnameValidator } from '../../../scripts/validation/surname';
import { nameValidator } from '../../../scripts/validation/name';
import { emailRegistrationValidator } from '../../../scripts/validation/email';
import { confirmPasswordValidator } from '../../../scripts/validation/password';
import { passwordValidator } from '../../../scripts/validation/password';
import { nameCompanyValidator } from '../../../scripts/validation/nameCompany';
import { Popup } from '../../../scripts/popup';

// Определение схемы валидации с использованием yup
const schema = yup.object().shape({
  surname: surnameValidator,
  name: nameValidator,
  name_company: nameCompanyValidator,
  password: passwordValidator,
  confirmation_password: confirmPasswordValidator,
  email: emailRegistrationValidator,
});

function FormSignUp() {
  const apiUrl = process.env.REACT_APP_API_URL;
  const navigate = useNavigate();
  const [currentImage, setCurrentImage] = useState(btnPass);
  const [inputType, setInputType] = useState('password');
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [currentConfirmImage, setCurrentConfirmImage] = useState(btnPass);
  const [inputConfirmType, setInputConfirmType] = useState('password');
  const [serverError, setServerError] = useState('');

  const {
    register,
    formState: { errors },
    handleSubmit,
  } = useForm({
    resolver: yupResolver(schema),
  });

  const onClickEye = () => {
    setCurrentImage(currentImage === btnPass ? btnPassVisib : btnPass);
    setInputType(inputType === 'text' ? 'password' : 'text');
  };

  const onClickConfirmEye = () => {
    setCurrentConfirmImage(currentConfirmImage === btnPass ? btnPassVisib : btnPass);
    setInputConfirmType(inputConfirmType === 'text' ? 'password' : 'text');
  };

  const onSubmit = async (data) => {
    setServerError('');
    fetch(`${apiUrl}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (response.ok) {
          setIsPopupOpen(true);
          setMessage('Ваша заявка отправлена на верификацию!');
          setTimeout(() => {
            navigate('/logIn'); // Переход на страницу входа после закрытия попапа
          }, 3100); // Задержка немного больше, чем время закрытия попапа, чтобы гарантировать переход после закрытия
        } else if(response.status===400) {
            setServerError('Эта почта уже зарегистрирована');
        }
      })
      .catch((error) => {
        console.error('Ошибка при регистрации:', error);
      });
  };
  const handleClose = () => {
    setIsPopupOpen(false);
  };

  return (
    <section className='container-sign-up'>
      <form className="form-container" onSubmit={handleSubmit(onSubmit)}>
        <h2>Регистрация</h2>
        {isPopupOpen && <Popup isOpen={isPopupOpen} message={message} onClose={handleClose} />}
        <div className='form-container-brim'>
          <div className='block-surname'>
            <label htmlFor="last-name">Фамилия</label>
            <input {...register("surname")} type="text" id="last-name" />
            {errors.surname && <p className='form-validation' style={{ color: 'red' }}>{errors.surname.message}</p>}
          </div>
          <div className='block-username'>
            <label htmlFor="name">Имя</label>
            <input {...register("name")} type="text" id="first-name" />
            {errors.name && <p className='form-validation' style={{ color: 'red' }}>{errors.name.message}</p>}
          </div>
          <div className='block-company'>
            <label htmlFor="name_company">Компания</label>
            <input {...register("name_company")} type="text" id="name-company" />
            {errors.name_company && <p className='form-validation' style={{ color: 'red' }}>{errors.name_company.message}</p>}
          </div>
          <div className='block-email'>
            <label htmlFor="email">Почта</label>
            <input {...register("email")} type="email" id="email" onChange={(e)=> setServerError('')}/>
            {errors.email && <p className='form-validation' style={{ color: 'red' }}>{errors.email.message}</p>}
            {serverError && <p style={{ color: 'red' }}>{serverError}</p>}
          </div>
          <div className='block-password'>
            <label htmlFor="password">Пароль</label>
            <input {...register("password")} className='js-input-password' type={inputType} id="password" />
            <img onClick={onClickEye} className='btn__pass js-btn-password' src={currentImage} alt='' />
            {errors.password && <p className='form-validation' style={{ color: 'red' }}>{errors.password.message}</p>}
          </div>
          <div className='block-confirm-password'>
            <label htmlFor="confirm-password">Повторите пароль</label>
            <input {...register("confirmation_password")} className='js-input-confirm-password' type={inputConfirmType} id="confirm-password" />
            <img onClick={onClickConfirmEye} className='btn__pass js-btn-password' src={currentConfirmImage} alt='' />
            {errors.confirmation_password && <p className='form-validation' style={{ color: 'red' }}>{errors.confirmation_password.message}</p>}
          </div>
          <button className='submit-form' type="submit">Зарегистрироваться</button>
        </div>
        <div className='block-registr'>
          <p>Уже есть аккаунт?</p>
          <Link to="/logIn" className="btn-registr"> <p>Войдите</p> </Link>
        </div>
      </form>
    </section>
  );
}

export default FormSignUp;