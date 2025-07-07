import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import './uploadFile.css';
import axios from 'axios';
import { Popup } from '../../scripts/popup';

const Spinner = () => (
    <div className="spinner-container">
        <div className="spinner"></div>
    </div>
);
const FormTest = () => {
    const [dockName, setDockName] = useState('');
    const [dockDescription, setDockDescription] = useState('');
    const [statusRequest, setStatusRequest] = useState('');
    const [loading, setLoading] = useState(false);
    const [serverError, setServerError] = useState('');
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const [message, setMessage] = useState('');
    const navigate = useNavigate();
    const apiUrl = process.env.REACT_APP_API_URL;
    const {
        register,
        reset,
        handleSubmit,
        formState: { isSubmitSuccessful }
    } = useForm();

    const onSubmitDock = async (data) => {
        setServerError('')
        const formDatas = new FormData();
        formDatas.append('file', data.files[0]);
        setLoading(true); // Показываем spinner
        try {
            const response = await fetch(`${apiUrl}/docks/upload-dock?dock_name=${dockName}&dock_description=${dockDescription}`, {
                method: 'POST',
                credentials: 'include',
                body: formDatas
            });
            const responseData = await response.json();
            if (!response.ok) {
                setServerError(`Возникла ошибка при загрузке документации, повторите загрузку`)
            }
            else if(response.ok){
                setIsPopupOpen(true);
                setMessage('Файл успешно добавлен в базу данных!');
            }
        } catch (error) {
            setStatusRequest(`Ошибка при отправке запроса: ${error}`);
        } finally {
            setLoading(false); // Скрываем spinner
        }
    };

    const handleCancel = () => {
        reset({
            dockName: '',
            dockDescription: '',
            files: null
        });
        setDockName('');
        setDockDescription('');
        setStatusRequest('');
        document.getElementById('files').value = '';
    };

    const handleClose = () => {
        setIsPopupOpen(false);
    };
    
    return (
        <section className='container-upload'>
            <form className='form-container-upload' action="#" method="POST" onSubmit={handleSubmit(onSubmitDock)}>
                <h2>Добавление документации</h2>
                {isPopupOpen && <Popup isOpen={isPopupOpen} message={message} onClose={handleClose} urlNavigate={'../work_documentation'}/>}
                <div className='upload-name'>
                    <label htmlFor="dockName">Название</label>
                    <input
                       {...register("dockName")} type="text" value={dockName} onChange={(e) => setDockName(e.target.value)} id="dock_name" name="dock_name" required />
                </div>
                <div className='upload-description'>
                    <label htmlFor="dockDescription">Описание</label>
                    <textarea
                        {...register("dockDescription")} type="text" value={dockDescription} onChange={(e) => setDockDescription(e.target.value)} id="dock_description" name="dock_description" required
                    />
                </div>
                <div className='upload-file'>
                    <input
                        {...register("files")} type="file" accept=".txt,.zip" id="files" name="files" required
                    />
                </div>
                {serverError && <p style={{ color: 'red' }}>{serverError}</p>}
                <div className='container-button'>
                    <button type="submit" className="btn-add button">
                        Отправить
                    </button>
                    <button type="button" className="button" onClick={handleCancel}>
                        Очистить
                    </button>
                    {loading && <Spinner />}
                </div>
            </form>
        </section>
    );
};

export default FormTest;
