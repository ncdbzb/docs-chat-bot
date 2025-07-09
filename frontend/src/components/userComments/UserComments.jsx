import { useForm } from 'react-hook-form';
import React, { useState, useRef, useEffect } from 'react';
import './userComments.css';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';

import likeIcon from '../../img/like.svg';
import dislikeIcon from '../../img/dislike.svg';
import closeForm from '../../img/close.svg';

const schema = yup.object().shape({
    feedbackText: yup.string().max(100, 'Максимальная длина 100 символов'),
});

export const UserComments = (props) => {
    const [feedbackTexts, setFeedbackTexts] = useState('');
    const [data, setData] = useState([]);
    const [feedback, setFeedback] = useState('');
    const [likeClicked, setLikeClicked] = useState(false);
    const [dislikeClicked, setDislikeClicked] = useState(false);
    const [showForm, setShowForm] = useState(false);
    const [statusRequest, setStatusRequest] = useState('');
    const [showPopup, setShowPopup] = useState(false);

    const [position, setPosition] = useState({ x: 100, y: 100 });
    const [isDragging, setIsDragging] = useState(false);
    const offset = useRef({ x: 0, y: 0 });

    const requestData = {
        value: feedback,
        user_comment: feedbackTexts,
        request_id: props.request_id
    };

    const apiUrl = process.env.REACT_APP_API_URL;
    const {
        register,
        reset,
        formState: { errors },
    } = useForm({
        resolver: yupResolver(schema),
    });

    const handleOnClickLike = () => {
        setFeedback('like');
        setLikeClicked(!likeClicked);
        setDislikeClicked(false);
        setShowForm(true);
    };

    const handleOnClickDislike = () => {
        setFeedback('dislike');
        setDislikeClicked(!dislikeClicked);
        setLikeClicked(false);
        setShowForm(true);
    };

    const handleOnClickClose = () => {
        setDislikeClicked(false);
        setLikeClicked(false);
        setShowForm(false);
        handleCancel();
    };

    const handleCancel = () => {
        reset({
            feedbackTexts: '',
        });
        setFeedbackTexts('');
        setStatusRequest('');
    };

    const fetchData = async () => {
        try {
            const response = await fetch(`${apiUrl}/send_feedback`, {
                method: 'POST',
                credentials: 'include',
                body: JSON.stringify(requestData),
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (response.ok) {
                setData(await response.json());
                handleOnClickClose();
                setShowPopup(true);
                setTimeout(() => {
                    setShowPopup(false);
                }, 3000); // Hide the popup after 3 seconds
            } else {
                console.error('Feedback request failed');
            }
        } catch (error) {
            console.error('Feedback error:', error);
        }
    };

    const handleMouseDown = (e) => {
        offset.current = {
            x: e.clientX - position.x,
            y: e.clientY - position.y
        };
        setIsDragging(true);
    };

    const handleMouseMove = (e) => {
        if (!isDragging) return;
        setPosition({
            x: e.clientX - offset.current.x,
            y: e.clientY - offset.current.y
        });
    };

    const handleMouseUp = () => {
        setIsDragging(false);
    };

    useEffect(() => {
        const handleMouseMoveDocument = (e) => {
            if (!isDragging) return;
            setPosition({
                x: e.clientX - offset.current.x,
                y: e.clientY - offset.current.y
            });
        };

        const handleMouseUpDocument = () => {
            setIsDragging(false);
        };

        document.addEventListener('mousemove', handleMouseMoveDocument);
        document.addEventListener('mouseup', handleMouseUpDocument);

        return () => {
            document.removeEventListener('mousemove', handleMouseMoveDocument);
            document.removeEventListener('mouseup', handleMouseUpDocument);
        };
    }, [isDragging]);

    return (
        <form className="feedback-container" action="#" method="POST">
            <div className='form-grade'>
                <img alt="like"
                    src={likeIcon}
                    onClick={handleOnClickLike}
                    style={{ filter: likeClicked ? 'none' : 'invert(70%)' }}
                />
                <img alt="dislike"
                    src={dislikeIcon}
                    onClick={handleOnClickDislike}
                    style={{ filter: dislikeClicked ? 'none' : 'invert(70%)' }}
                />
            </div>
            {showForm && (
                <div
                    className='form-feedback'
                    style={{ top: `${position.y}px`, left: `${position.x}px`, position: 'absolute' }}
                    onMouseDown={handleMouseDown}
                >
                    <div className='form-feedback-block'>
                        <div className='form-feedback-block-title'>
                            <div className="feedbackText" htmlFor="feedbackText">Обратная связь</div>
                            <img alt='close-icon'
                                src={closeForm}
                                onClick={handleOnClickClose}
                            />
                        </div>
                        <div className="textarea-container">
                            <textarea
                                {...register("feedbackText")}
                                type="text"
                                value={feedbackTexts}
                                onChange={(e) => setFeedbackTexts(e.target.value)}
                                id="feedbackText"
                                name="feedbackText"
                                maxLength="300"
                                required
                            />
                            <div className="char-count">
                                {feedbackTexts.length}/300
                            </div>
                        </div>
                        {errors.feedbackText && <p className='form-validation' style={{ color: 'red' }}>{errors.feedbackText.message}</p>}
                    </div>
                    <div className='container-button'>
                        <button type='button' className="btn-add" onClick={fetchData}>Отправить</button>
                        <button type='button' className="button" onClick={handleCancel}>Очистить</button>
                    </div>
                </div>
            )}
            {showPopup && (
                <div className="popup-user-comment">
                    Спасибо за вашу оценку
                </div>
            )}
        </form>
    );
};