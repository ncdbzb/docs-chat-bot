import { useForm } from 'react-hook-form';
import React, { useState, useEffect } from 'react';
import '../../components/personArea/mainPersonArea/informationUser.css';
import { feedbackViewed } from './FeedbackViewed';

const ListFeedback = () => {
    const [data, setData] = useState([]);
    const [isOpen, setIsOpen] = useState(false);

    const apiUrl = process.env.REACT_APP_API_URL;
    const apiUrlFront = process.env.REACT_APP_API_FRONT_URL;
    const {
        register,
        reset,
        handleSubmit,
    } = useForm();


    const toggleDropdown = async (flag) => {
        if (!isOpen) {
            try {
                // Отправка запроса при открытии списка
                const response = await fetch(`${apiUrl}/admin/get_feedback?all_feedbacks=${flag}`, {
                    method: 'POST',
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

    const feedbackViewed = (id) => {
        feedbackViewed(id);
    }


    return (
        <div className="dropdown-container">
            <div>Фитбеки</div>
            <div className="dropdown">
                <div className='btn-feedback-container'>
                    <a onClick={() => (toggleDropdown(true))}>Все фитбеки</a>
                    <a onClick={() => (toggleDropdown(false))}>Не просмотрененные фитбеки</a>
                </div>
                {isOpen && data.length > 0 && (
                    <ul>
                        {data.map((item, index) => (
                            <li key={index}>
                                {item['value']} {item['user_comment']} <br/>
                                {item['llm_response']}
                                <button feedbackViewed={ () => (feedbackViewed(item['id'])) }>Просмотрено</button>
                            </li>
                        ))}
                    </ul>
                )}
                {isOpen && data.length === 0 && (
                    <div>Нет пользователей на верефикацию</div>
                )}
            </div>
        </div>
    );
}

export default ListFeedback;
