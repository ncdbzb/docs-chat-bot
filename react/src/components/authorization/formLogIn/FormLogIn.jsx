import { useForm } from 'react-hook-form';
import React, { useState, useEffect } from 'react';
import './formLogIn.css';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { useAuth } from '../../../scripts/usersMe';
import btnPass from '../../../img/icons/password/Visibility=True.svg';
import btnPassVisib from '../../../img/icons/password/Visibility=False.svg';
import { emailRegistrationValidator } from '../../../scripts/validation/email';
import { Popup } from '../../../scripts/popup';

const schema = yup.object().shape({
    email: emailRegistrationValidator,
    password: yup
    .string()
    .required('Пароль обязателен')    
});

async function verifyToken({token, setMessage, setIsPopupOpen}) {
    const apiUrl = process.env.REACT_APP_API_URL;
    // Здесь должна быть логика проверки токена
    // Например, запрос на ваш сервер для проверки токена
    try {
        const response = await fetch(`${apiUrl}/auth/verify/${token}`, {
            method: "GET",
            credentials: "include",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        setIsPopupOpen(true);
        setMessage('Верификация прошла успешно!');
    } catch (error) {
        console.error("Error fetching user data:", error);
    } finally {
        
    }
    return false;
}


function VerifyUserComponent({ token, onVerificationComplete, setMessage, setIsPopupOpen }) {
    useEffect(() => {
        const validate = async () => {
            const isValid = await verifyToken({token,setMessage, setIsPopupOpen});
            if (isValid) {
                
            }
            onVerificationComplete();
        };
        validate();
    }, [token, onVerificationComplete]);

    return null;
}

export default function FormLogIn() {
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const [message, setMessage] = useState('');
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const token = searchParams.get('token');
    const [verificationComplete, setVerificationComplete] = useState(!token);
    const [currentImage, setCurrentImage] = useState(btnPass);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [inputType, setInputType] = useState('password');
    const [serverError, setServerError] = useState('');
    const apiUrl = process.env.REACT_APP_API_URL;
    const {
        register,
        formState: { errors },
        handleSubmit,
    } = useForm({
        resolver: yupResolver(schema),
    });

    const navigate = useNavigate();

    const onClickEye = () => {
        setCurrentImage(currentImage === btnPass ? btnPassVisib : btnPass);
        setInputType(inputType === 'text' ? 'password' : 'text');
    };

    const onSubmit = async (data) => {
        setServerError('');
        try {
            const response = await fetch(`${apiUrl}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'grant_type': '',
                    'username': data.email,
                    'password': data.password,
                    'scope': '',
                    'client_id': '',
                    'client_secret': '',
                }).toString(),
                credentials: 'include',
            });
            if(response.ok){
                navigate('/');
            }
            else if (response.status===400) {
                setServerError(`Неверная почта или пароль`)
            }
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    };

    const handleClose = () => {
        setIsPopupOpen(false);
      };
    return (
        <section className='container-log-in'>
            {isPopupOpen && <Popup isOpen={isPopupOpen} message={message} onClose={handleClose} />}
            {token && !verificationComplete && (
                <VerifyUserComponent
                    token={token}
                    onVerificationComplete={() => setVerificationComplete(true)}
                    setIsPopupOpen={setIsPopupOpen}
                    setMessage={setMessage}
                />
            )}
            {verificationComplete && (
                <form className="form-container" action="#" method="POST" onSubmit={handleSubmit(onSubmit)}>
                    <h2>Вход</h2>
                    <div className='form-container-brim'>
                        <div className='block-email'>
                            <label className='email' htmlFor="email">Почта</label>
                            <input {...register("email")} type="email" id="email" />
                            {errors.email && <p className='form-validation' style={{ color: 'red' }}>{errors.email.message}</p>}
                        </div>
                        <div className='block-password'>
                            <label htmlFor="password">Пароль</label>
                            <input {...register("password")} className='js-input-password' type={inputType} id="password" />
                            <img onClick={onClickEye} className='btn__pass js-btn-password' src={currentImage} alt='' fill='none' />
                            {errors.password && <p className='form-validation' style={{ color: 'red' }}>{errors.password.message}</p>}
                            {serverError && <p style={{ color: 'red' }}>{serverError}</p>}
                        </div>
                        <button className='submit-form' type="submit">Войти</button>
                    </div>
                    <Link to="/forgot_password" className="btn-forgot"> <p>Не помню пароль</p> </Link>
                    <div className='block-registr'>
                        <p>Нет аккаунта?</p>
                        <Link to="/signUp" className="btn-registr"> <p>Зарегистрируйтесь</p> </Link>
                    </div>
                </form>
            )}
        </section>
    );
}