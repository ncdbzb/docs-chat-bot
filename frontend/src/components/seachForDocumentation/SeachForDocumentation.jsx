import { useForm } from 'react-hook-form';
import React, { useState, useEffect } from 'react';
import './seachForDocumentation.css';
import { useAuth } from '../../scripts/usersMe';
import { RemovingDocumentation } from '../../scripts/removingDocumentation';
import btnEdit from '../../img/edit.svg';
import FormEditDocumentation from '../workDocumentation/editDocumentation/FormEditDocumentation';
import { AddDocumentation } from '../workDocumentation/editDocumentation/addDocumentation/addDocumentation';
const SeachForDocumentation = ({ onClick }) => {
    const { userData, isAuthChecked } = useAuth(); // Состояние isLoggedIn
    const [data, setData] = useState([]);
    const [isOpen, setIsOpen] = useState(true);
    const [popupInform, setPopupInform] = useState(''); // Добавленное состояние для попапа
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [docToDelete, setDocToDelete] = useState(null);
    const [fileName, setFileName] = useState();
    const apiUrl = process.env.REACT_APP_API_URL;
    const apiUrlFront = process.env.REACT_APP_API_FRONT_URL;
    const { register, reset, handleSubmit } = useForm();
    const [isEditingSave, setIsEditingSave] = useState(false);
    const [addFile, setAddFile] = useState(false);

    const copyTextToClipboard = async (text) => {
        try {
            await navigator.clipboard.writeText(text);
            setPopupInform('Ссылка успешно скопирована в буфер обмена');
            setTimeout(() => {
                setPopupInform(''); // Скрыть попап через 2 секунды
            }, 2000);
        } catch (err) {
            console.error('Ошибка:', err);
        }
    };

    const clickLink = (item) => {
        copyTextToClipboard(`${apiUrlFront}/request_documentation?documentation=${item['name']}`);
    };

    let userUrl = 'my';
    if (userData.is_superuser) {
        userUrl = 'all';
    }

    useEffect(() => {
        if (isAuthChecked) {
            const fetchData = async () => {
                try {
                    // Отправка запроса при загрузке страницы
                    const response = await fetch(`${apiUrl}/docks/${userUrl}`, {
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
            };

            fetchData();
        }
    }, [isAuthChecked, apiUrl, userUrl]);

    const confirmDelete = (doc_name) => {
        setDocToDelete(doc_name);
        setShowConfirmation(true);
    };

    const handleDelete = () => {
        RemovingDocumentation(docToDelete);
        setShowConfirmation(false);
        setDocToDelete(null);
    };

    const handleCancelDelete = () => {
        setShowConfirmation(false);
        setDocToDelete(null);
    };
    const handleEditClickSave = (flagWindowEdit, fileName) => {
        setIsEditingSave(flagWindowEdit)
        setFileName(fileName)
    }
    const handleAddClickSave = (flagWindowAdd, fileName) => {
        setFileName(fileName)
        setAddFile(flagWindowAdd)
    }
    if (!isAuthChecked) {
        return null;
    }

    return (
        <div className="dropdown-container">
            <div className="dropdown">
                {isOpen && data.length > 0 ? (
                    <ul className='documentation-list'>
                        {popupInform && <div className='document-popup'>{popupInform}</div>}
                        {data.map((item, index) => (
                            <li key={index} className='documentation-list-item'>
                                <div className='container-edit-file'>
                                    <h3 className='title'>{item['name']}</h3>
                                    <a onClick={() => handleEditClickSave(true,item['name'] )}>
                                            <img src={btnEdit} alt='Edit' />
                                    </a>
                                </div>                               
                                <p className='description'>{item['description']}</p>
                                <div className='container-button'>
                                    <button className='btn-add' onClick={() => clickLink(item)}>
                                        Получить ссылку
                                    </button>
                                    <button className="button" onClick={() => handleAddClickSave(true,item['name'] )}>Дополнить</button>
                                    <button className="button" onClick={() => confirmDelete(item['name'])}>
                                        Удалить документацию
                                    </button>
                                </div>
                                {(isEditingSave && item['name']===fileName) && (
                                    <FormEditDocumentation docName={item['name']} description={item['description']} onClose={handleEditClickSave}/>
                                    
                                )}
                                {(addFile && item['name']===fileName) && (
                                    <AddDocumentation docName={item['name']} onClose={handleAddClickSave}/>
                                )}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <div>Вы не добавили ни одной документации</div>
                )}
            </div>
            {showConfirmation && (
                <div className="confirmation-popup">
                    <div className="confirmation-content">
                        <p>Вы уверены, что хотите удалить эту документацию?</p>
                        <div className='container-button'> 
                            <button className="confirm-button button" onClick={handleDelete}>
                                Да
                            </button>
                            <button className="cancel-button button" onClick={handleCancelDelete}>
                                Отмена
                            </button>
                        </div> 
                    </div>
                </div>
            )}
        </div>
    );
};

export default SeachForDocumentation;