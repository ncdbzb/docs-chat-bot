import { useForm } from 'react-hook-form';
import { useState } from 'react';
import { useRequestAddDocumentation } from './requestAddDocumentation';
import iconClose from '../../../../img/icons/cross.svg';
import { Popup } from '../../../../scripts/popup';

export const AddDocumentation = ({ docName, onClose }) => {
    const {
        register,
        reset,
        handleSubmit,
        formState: { errors },
    } = useForm();
    const { sendRequest, isLoggedIn } = useRequestAddDocumentation();
    const [message, setMessage] = useState('');
    const [flag, setFlag] = useState(false);

    const handleClose = () => {
        onClose(false);
        reset({
            files: null,
        });
    };

    const onSubmit = async (data) => {
        try {
            await sendRequest({ docName, file: data.files[0], setFlag, setMessage });
        } catch (error) {
            console.error('Failed to send request:', error);
        }
    };

    return (
        <form className="form-container-upload" action="#" method="POST" onSubmit={handleSubmit(onSubmit)}>
            {flag && <Popup isOpen={flag} message={message} onClose={handleClose} useNavigate={'./work_documentation'}/>}
            <div className='container-close'>
                <h2>Добавление данных в документацию</h2>
                <a className='link-close' onClick={handleClose}>
                    <img src={iconClose} alt="Close" />
                </a>
            </div>
            <div className='upload-file'>
                <input
                    {...register("files")} type="file" accept=".txt" id="files" name="files" required
                />
            </div>
            <button className="btn-add" type='submit'>Сохранить</button>
        </form>
    );
};