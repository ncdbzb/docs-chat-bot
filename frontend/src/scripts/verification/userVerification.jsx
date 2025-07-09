import { useForm } from 'react-hook-form';
import React, { useState, useEffect } from 'react';
import '../../components/personArea/mainPersonArea/informationUser.css';
import { AcceptRequest } from './acceptRequest';
import { RejectRequest } from './rejectRequest';
import { Popup } from '../popup';

const UserVerification = ({ onClick }) => {
    const [data, setData] = useState([]);
    const [isOpen, setIsOpen] = useState(false);
    const [message, setMessage] = useState('');
    const [flagAccept, setFlagAccept] = useState(false);
    const [flagReject, setFlagReject] = useState(false);
    const apiUrl = process.env.REACT_APP_API_URL;

    const{
        handleSubmit,
    } = useForm();

    const toggleDropdown = async () => {
        if (!isOpen) {
            try {
                // Отправка запроса при открытии списка
                const response = await fetch(`${apiUrl}/admin/requests`, {
                    method: 'GET',
                    credentials: 'include', // Убедитесь, что куки прикрепляются к запросу
                });
                if (response.ok) {
                    setData(await response.json());
                } else {
                    console.error('Проблема поиска');
                }
            } catch (error) {
                console.error('Ошибка:', error);
            }
        }
        setIsOpen(!isOpen);
    };

    const acceptRequest = (id) => {
        AcceptRequest({ id, setFlagAccept, setMessage });
    }

    const rejectRequest = (id) => {
        RejectRequest(id, setFlagReject, setMessage);
    }

    const handleClose = () => {
        setFlagAccept(false);
        setFlagReject(false);
        window.location.reload();
    };

    return (
        <div className="dropdown-container">
            <div className="dropdown">
                {flagAccept && <Popup isOpen={flagAccept} message={message} onClose={handleClose} />}
                {flagReject && <Popup isOpen={flagReject} message={message} onClose={handleClose} />}
                <button className='user-verification' onClick={toggleDropdown}>Пользователи на верификацию</button>
                {isOpen && data.length > 0 && (
                    <ul className='verf-list'>
                        {data.map((item, index) => (
                            <li className='verf-list-item' key={index}>
                                <div className='verf-item-inform'>
                                    <div className='inform-user'>
                                        <p>{item['info'].name}</p>
                                        <p>{item['info'].surname}</p>
                                    </div>
                                    <div className='verf-item-email'>
                                        <p>{item['info'].email}</p>
                                    </div>
                                </div>
                                <div className='verf-item-block-btn container-button'>
                                    <button className='button' onClick={() => acceptRequest(item['id'])}>Принять</button>
                                    <button className='button' onClick={() => rejectRequest(item['id'])}>Отклонить</button>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
                {isOpen && data.length === 0 && (
                    <div>Нет пользователей на верификацию</div>
                )}
            </div>
        </div>
    );
}

export default UserVerification;