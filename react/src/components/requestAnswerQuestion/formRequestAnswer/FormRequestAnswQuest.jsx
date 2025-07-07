import { useForm } from 'react-hook-form';
import React, { useState, useRef, useEffect } from 'react';
import './formRequestAnswQuest.css';
import icomSubmitQuest from '../../../img/icons/Icon-color.svg';
import { UserComments } from '../../userComments/UserComments';

const Spinner = () => (
    <div className="spinner-container">
        <div className="spinner"></div>
    </div>
);

const FormRequestAnswQuest = ({ docName }) => {
    const formRef = useRef(null);
    const answersListRef = useRef(null); // Reference for the answers list
    const [massivAnswer, setMassivAnswer] = useState(JSON.parse(localStorage.getItem(`${docName}`)) || []);
    const [id, setId] = useState('');
    const [result, setResult] = useState('');
    const [question, setQuestion] = useState('');
    const [loading, setLoading] = useState(false);
    const textareaRef = useRef(null);
    const [serverError, setServerError] = useState('');
    const apiUrl = process.env.REACT_APP_API_URL;
    const { register, reset, handleSubmit } = useForm();
    const addItem = (newItem) => {
        setMassivAnswer((prevItems) => [...prevItems, newItem]);
    };

    useEffect(() => {
        localStorage.setItem(`${docName}`, JSON.stringify(massivAnswer));
    }, [massivAnswer, docName]); // Зависимость от massivAnswer и docName

    const handleCancel = () => {
        reset({
            question: '',
        });
        setQuestion('');
    };

    const formatAnswer = (answer) => {
        if (answer.includes('\n\n')) {
            const steps = answer.split('\n').map((step, index) => {
                return <p key={index}>{step}</p>;
            });
            return <div className="formatted-answer">{steps}</div>;
        }
        return <p>{answer}</p>;
    };

    const onSubmitTest = async () => {
        setServerError('');
        setLoading(true); // Показываем спиннер
        try {
            const response = await fetch(`${apiUrl}/get_answer?filename=${docName}&question=${question}`, {
                method: 'POST',
                credentials: 'include',
            });
            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('Пожалуйста, авторизируйтесь!');
                } else {
                    throw new Error('Произошла ошибка при генерации теста, попробуйте заново');
                }
            }

            const responseData = await response.json();
            handleCancel();
            addItem(responseData['result']); // Получение данных из ответа
            setId(responseData['request_id']);
            setResult(responseData['result']);
        } catch (error) {
            setServerError(error.message);
        } finally {
            setLoading(false); // Скрываем спиннер
        }
    };

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = '22px'; // Сброс высоты для вычисления
            let newHeight = textareaRef.current.scrollHeight - 20;

            if (newHeight > 450) {
                textareaRef.current.style.height = '450px';
                textareaRef.current.style.overflowY = 'auto'; // Добавляем вертикальный скролл
            } else {
                textareaRef.current.style.height = `${newHeight}px`;
                textareaRef.current.style.overflowY = 'hidden'; // Убираем вертикальный скролл
            }
        }
    }, [question]);

    useEffect(() => {
        if (answersListRef.current) {
            answersListRef.current.scrollTop = answersListRef.current.scrollHeight;
        }
    }, [massivAnswer]); // Scroll to bottom whenever massivAnswer changes

    const handleKeyDown = (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSubmit(onSubmitTest)();
        }
    };

    return (
        <section className='container-work-documentation'>
            <form className='form-container-question block-form-request' ref={formRef} action="#" method="POST" onSubmit={handleSubmit(onSubmitTest)}>
                <h2>Ответы на основе документации <span>{docName}</span></h2>

                <div className="answers-list" ref={answersListRef}>
                    {serverError && <p style={{ color: 'red' }}>{serverError}</p>}
                    {massivAnswer.map((item, index) => (
                        <>
                            <div className="questions-container">
                                {localStorage.setItem('itemQuestion', item.question)}
                                <p>{localStorage.getItem('itemQuestion')}</p>
                            </div>
                            <div className="answer-container">
                                {formatAnswer(item.answer)}
                                <UserComments request_id={id} result={result} />
                            </div>
                        </>
                    ))}
                </div>
                <div className='block-input'>
                    <textarea
                        {...register("question")}
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        ref={textareaRef}
                        id="question"
                        placeholder='Ваш вопрос'
                        name="question"
                        required
                        onKeyDown={handleKeyDown} // Добавляем обработчик события onKeyDown
                    />
                    <button type='submit' disabled={loading} style={{ display: loading ? 'none' : 'block' }}>
                        <img src={icomSubmitQuest} className='iconSubmitQuest' alt='' />
                    </button>
                    {loading && <Spinner />}
                </div>
                <p className='disclaimer'> Наш цифровой помощник находится на стадии опытного экземпляра, и нам очень важна ваша помощь в его улучшении. 
                    Если вы заметили некорректные формулировки, фактические ошибки или другие недочеты в вопросах или ответах, пожалуйста, оставьте аргументированную обратную связь, нажав на кнопку лайка или дизлайка.
                    Ваши отзывы помогут нам сделать нашего помощника лучше и полезнее. Спасибо за участие!
                </p>
            </form>
        </section>
    );
};

export default FormRequestAnswQuest;
