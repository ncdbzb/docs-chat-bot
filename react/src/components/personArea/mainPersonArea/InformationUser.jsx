import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './informationUser.css';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { useForm } from 'react-hook-form';
import { useAuth } from '../../../scripts/usersMe';
import UserVerification from '../../../scripts/verification/userVerification';
import btnPass from '../../../img/icons/password/Visibility=True.svg';
import btnPassVisib from '../../../img/icons/password/Visibility=False.svg';
import btnEdit from '../../../img/edit.svg';
import Leaderboard from '../leaderboard/Leaderboard';
import { ResetPasswordLK } from '../../forgotPassword/resetPassword/ResetPasswordLK';
import { surnameValidator } from '../../../scripts/validation/surname';
import { nameValidator } from '../../../scripts/validation/name';
import { emailRegistrationValidator } from '../../../scripts/validation/email';
import { confirmPasswordValidator } from '../../../scripts/validation/password';
import { passwordValidator } from '../../../scripts/validation/password';
import { Popup } from '../../../scripts/popup';

const editSchema = yup.object().shape({
  surname: surnameValidator,
  name: nameValidator,
  email: emailRegistrationValidator,
});

const passwordSchema = yup.object().shape({
  old_password: passwordValidator,
  password: passwordValidator,
  confirmation_password: confirmPasswordValidator,
});

const InformationUser = () => {
    const { userData } = useAuth();
    const [isEditing, setIsEditing] = useState(false);
    const [isEditingSave, setIsEditingSave] = useState(false);
    const [password, setPassword] = useState('');
    const [surname, setSurname] = useState('');
    const [name, setName] = useState('');
    const [email, setEmail] = useState('')
    const [flag,setFlag] = useState(false);
    const [message, setMessage] = useState('');
    const [old_password, setCurrentPassword] = useState('');
    const [confirmation_password, setConfirmPassword] = useState('');
    const [currentImage, setCurrentImage] = useState(btnPass);
    const [inputType, setInputType] = useState('password');
    const [currentCurrentImage, setCurrentCurrentImage] = useState(btnPass);
    const [inputCurrentType, setInputCurrentType] = useState('password');
    const [currentConfirmImage, setCurrentConfirmImage] = useState(btnPass);
    const [inputConfirmType, setInputConfirmType] = useState('password');
    const [serverErrorEmail, setServerErrorEmail] = useState('');
    const [serverErrorPassword, setServerErrorPassword] = useState('');
    
    const {
      register: registerEdit,
      handleSubmit: handleSubmitEdit,
      reset: resetEdit,
      formState: { errors: editErrors }
    } = useForm({
      resolver: yupResolver(editSchema),
    });

    const {
      register: registerPassword,
      handleSubmit: handleSubmitPassword,
      reset: resetPassword,
      formState: { errors: passwordErrors }
    } = useForm({
      resolver: yupResolver(passwordSchema),
    });

    const handleEditClick = () => {
        setIsEditing(true);
    };

    const handleEditClickSave = () => {
        setIsEditingSave(true);
    };

    const handleCancelEdit = () => {
        resetEdit({
            surname: userData.surname,
            name: userData.name,
            email: userData.email,
        });
        setIsEditingSave(false);
        setServerErrorEmail('');
    };

    const handleCancelPassword = () => {
        resetPassword({
            old_password: '',
            password: '',
            confirmation_password: '',
        });
        setCurrentPassword('');
        setPassword('');
        setConfirmPassword('');
        setIsEditing(false);
        setServerErrorPassword('');
    };

    const onSubmitEdit = async (data) => {
        const result = await ResetPasswordLK({data, setMessage, setFlag});
        if (result && result.error) {
            setServerErrorEmail(result.error);
        }
    };

    const onSubmitPassword = async (data) => {
        const result = await ResetPasswordLK({data, setMessage, setFlag});
        if (result && result.error) {
            setServerErrorPassword(result.error);
        } else {
            setIsEditing(false);
        }
    };
    const handleClose = () => {
        setFlag(false)
        window.location.reload();
      };

    const onClickEye = () => {
        setCurrentImage(currentImage === btnPass ? btnPassVisib : btnPass);
        setInputType(inputType === 'text' ? 'password' : 'text');
    };

    const onClickConfirmEye = () => {
        setCurrentConfirmImage(currentConfirmImage === btnPass ? btnPassVisib : btnPass);
        setInputConfirmType(inputConfirmType === 'text' ? 'password' : 'text');
    };

    const onClickCurrentEye = () => {
        setCurrentCurrentImage(currentCurrentImage === btnPass ? btnPassVisib : btnPass);
        setInputCurrentType(inputCurrentType === 'text' ? 'password' : 'text');
    };

    return (
        <section className='container-person-area'>
            {flag && <Popup isOpen={flag} message={message} onClose={handleClose}/>}
            <div className='person-area-user'>
                <h2>Личные данные</h2>
                {!isEditingSave ? (
                    <>
                        {userData.is_superuser ? (
                            <div className='admin-panel'>
                                <div className='user-information'>
                                    <div className='user-img'></div>
                                    <div className='inform-list'>
                                        <div className='inform-list-item'>
                                            <div>{userData.name} {userData.surname}</div>
                                            <div>{userData.email}</div>
                                            <div>Админ</div>
                                        </div>
                                        <a onClick={handleEditClickSave}>
                                            <img src={btnEdit} alt='Edit' />
                                        </a>
                                    </div>
                                </div>
                                <div className='verification-container'>
                                    <UserVerification />
                                </div>
                            </div>
                        ) : (
                            <div className='user-information'>
                                <div className='user-img'></div>
                                <div className='inform-list'>
                                    <div className='inform-list-item'>
                                        <div>{userData.name} {userData.surname}</div>
                                        <div>{userData.email}</div>
                                        <div>Сотрудник компании</div>
                                    </div>
                                    <a onClick={handleEditClickSave}>
                                        <img src={btnEdit} alt='Edit' />
                                    </a>
                                </div>
                            </div>
                        )}
                    </>
                ) : (
                    <form className="form-container edit-form" onSubmit={handleSubmitEdit(onSubmitEdit)}>
                        <div className='form-container-brim'>
                            <div className='block-surname'>
                                <label htmlFor="last-name">Фамилия</label>
                                <input {...registerEdit("surname")} type="text" id="last-name" defaultValue={userData.surname || ''} onChange={(e)=>setSurname(e.target.value)}/>
                                {editErrors.surname && <p className='form-validation' style={{ color: 'red' }}>{editErrors.surname.message}</p>}
                            </div>
                            <div className='block-username'>
                                <label htmlFor="first-name">Имя</label>
                                <input {...registerEdit("name")} type="text" id="first-name" defaultValue={userData.name || ''} onChange={(e)=>setName(e.target.value)} />
                                {editErrors.name && <p className='form-validation' style={{ color: 'red' }}>{editErrors.name.message}</p>}
                            </div>
                            <div className='block-email'>
                                <label htmlFor="email">Почта</label>
                                <input {...registerEdit("email")} type="email" id="email" defaultValue={userData.email || ''} onChange={(e)=>setEmail(e.target.value)} />
                                {editErrors.email && <p className='form-validation' style={{ color: 'red' }}>{editErrors.email.message}</p>}
                                {serverErrorEmail && <p className='form-validation' style={{ color: 'red' }}>{serverErrorEmail}</p>}
                            </div>
                            <div className='container-button'>
                              <button className='submit-form' type="submit">Сохранить</button>
                              <button type="button" className="button" onClick={handleCancelEdit}>Отменить</button>
                            </div>
                        </div>
                    </form>
                )}
            </div>
            {!isEditing ? (
                <div className='user-edit'>
                    <h3>Пароль</h3>
                    <div className='container-edit-btn'>
                        <button className='edit-password button' onClick={handleEditClick}>
                            Изменить
                        </button>
                    </div>
                </div>
            ) : (
                <form className="form-container edit-form password-form" onSubmit={handleSubmitPassword(onSubmitPassword)}>
                    <div className='container-edit-info'>
                        <h3>Изменение пароля</h3>
                    </div>
                    <div className='block-current-password password'>
                        <label htmlFor="old_password">Текущий пароль</label>
                        <input {...registerPassword("old_password")} className='js-input-current-password' value={old_password} onChange={(e) => {setServerErrorPassword(''); setCurrentPassword(e.target.value)}} type={inputCurrentType} id="current-password" name="old_password" />
                        <img onClick={onClickCurrentEye} className='btn__pass js-btn-password' src={currentCurrentImage} alt='' />
                        {passwordErrors.old_password && <p className='form-validation' style={{ color: 'red' }}>{passwordErrors.old_password.message}</p>}
                        {serverErrorPassword && <p className='form-validation' style={{ color: 'red' }}>{serverErrorPassword}</p>}
                    </div>
                    <div className='block-password password'>
                        <label htmlFor="password">Новый пароль</label>
                        <input {...registerPassword("password")} className='js-input-password' value={password} onChange={(e) => setPassword(e.target.value)} type={inputType} id="password" name="password" />
                        <img onClick={onClickEye} className='btn__pass js-btn-password' src={currentImage} alt='' />
                        {passwordErrors.password && <p className='form-validation' style={{ color: 'red' }}>{passwordErrors.password.message}</p>}
                    </div>
                    <div className='block-confirm-password password'>
                        <label htmlFor="confirmation_password">Повторите новый пароль</label>
                        <input {...registerPassword("confirmation_password")} className='js-input-confirm-password' value={confirmation_password} onChange={(e) => setConfirmPassword(e.target.value)} type={inputConfirmType} id="confirm-password" name='confirmation_password' />
                        <img onClick={onClickConfirmEye} className='btn__pass js-btn-password' src={currentConfirmImage} alt='' />
                        {passwordErrors.confirmation_password && <p className='form-validation' style={{ color: 'red' }}>{passwordErrors.confirmation_password.message}</p>}
                    </div>
                    <div className='container-button'>
                        <button type="submit" className="btn-add">Отправить</button>
                        <button type="button" className="button" onClick={handleCancelPassword}>Отменить</button>
                    </div>
                </form>
            )}
            <Leaderboard />
        </section>
    );
};

export default InformationUser;
