import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import '../workDocumentation/workDocumentation/workDocumentation.css';
import { UserComments } from '../userComments/UserComments';

const Spinner = () => (
    <div className="spinner-container">
        <div className="spinner"></div>
    </div>
);

const FormRequestsTest = (props) => {
    const [questionData, setQuestionData] = useState(JSON.parse(localStorage.getItem('storageTest') || null));
    const [selectedAnswer, setSelectedAnswer] = useState('');
    const [id, setId] = useState(localStorage.getItem('idRequest') ||'');
    const [result, setResult] = useState('');
    const [answerServer, setAnswerServer] = useState(localStorage.getItem('rightAnswer') ||'');
    const [loading, setLoading] = useState(false);
    const [serverError, setServerError] = useState('');
    const apiUrl = process.env.REACT_APP_API_URL;
    const { handleSubmit } = useForm();
    const onSubmitTest = async () => {
        setServerError('');
        setLoading(true);

        try {
             // Отправляем запрос только если данные еще не загружены
                const response = await fetch(`${apiUrl}/get_test?filename=${props.docName}`, {
                    method: 'POST',
                    credentials: 'include',
                });

                if(response.status===401){
                    setServerError('Чтобы сгенировать тест авторизируйтесь');
                }
                else if (response.status===502) {
                    setServerError('Произошла ошибка при генерации теста, попробуйте заново');
                }
                localStorage.removeItem('rightAnswer'); 
                const responseData = await response.json();
                localStorage.setItem('storageTest',JSON.stringify(responseData.result))
                localStorage.setItem('idRequest',JSON.stringify(responseData.request_id))
                setQuestionData(responseData.result);
                setId(responseData.request_id);
                setResult(responseData.result);
                setSelectedAnswer('');
                setAnswerServer('');
            
        } catch (error) {
            setServerError(error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleAnswerSelection = async (answer) => {
        setSelectedAnswer(answer);
        setServerError('');
        try {
            if (!answerServer) { // Используем хранящийся правильный ответ, если он уже есть
                const response = await fetch(`${apiUrl}/check_test`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        request_id: id,
                        selected_option: answer,
                    }),
                });

                if (!response.ok) {
                    throw new Error('Произошла ошибка при проверке ответа');
                }

                const responseData = await response.json();
                setAnswerServer(responseData.right_answer);
                localStorage.setItem('rightAnswer', responseData.right_answer)
            }
        } catch (error) {
            setServerError(error.message);
        } finally {
        }
    };

    return (
        <section className='container-work-documentation'>
            <form className='form-container-test block-form-request' onSubmit={handleSubmit(onSubmitTest)}>
                <h2>Тесты на основе документации <span>{props.docName}</span></h2>
                {serverError && <p style={{ color: 'red' }}>{serverError}</p>}
                <button className='btn-add button-test' type="submit" disabled={loading}>
                    Сгенерировать тест
                </button>
                {loading && <Spinner />}
                {questionData && (
                    <div className='question-container'>
                        <h3>{questionData.question}</h3>
                        <ul className='test-list'>
                            {['1 option', '2 option', '3 option', '4 option'].map((optionKey, index) => (
                                <li
                                    key={index}
                                    className={`test-list-item ${
                                        answerServer === questionData[optionKey] ? 'answer-right' :
                                        selectedAnswer === questionData[optionKey] ? 'answer-wrong' : ''
                                    }`}
                                    onClick={() => handleAnswerSelection(questionData[optionKey])}
                                    style={{ cursor: 'pointer' }}
                                >
                                    {questionData[optionKey]}
                                </li>
                            ))}
                        </ul>
                        <UserComments request_id={id} result={result} />
                    </div>
                )}
                <p className='disclaimer'> Наш цифровой помощник находится на стадии опытного экземпляра, и нам очень важна ваша помощь в его улучшении. 
                    Если вы заметили некорректные формулировки, фактические ошибки или другие недочеты в вопросах или ответах, пожалуйста, оставьте аргументированную обратную связь, нажав на кнопку лайка или дизлайка.
                    Ваши отзывы помогут нам сделать нашего помощника лучше и полезнее. Спасибо за участие!
                </p>
            </form>
        </section>
    );
};

export default FormRequestsTest;

