import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import './workDocumentation.css';
import SeachForDocumentation from '../../seachForDocumentation/SeachForDocumentation';
import iconAdd from '../../../img/icons/Add.svg';
import { useNavigate } from 'react-router-dom';

const WorkDocumentation = () => {
    const [flagTestOrAnswer, setFlagTestOrAnswer] = useState(false);
    const [id, setId] = useState('');
    const [result, setResult] = useState('');
    const { register, handleSubmit } = useForm();
    const navigate = useNavigate();

    const onClickTest = () => {
        setFlagTestOrAnswer(false);
    };
    const onClickAnswer = () => {
        setFlagTestOrAnswer(true);
    };

    const handleUploadClick = () => {
        navigate('/upload_file');
    };

    return (
        <section className='container-documentation'>
            <h2>Мои документации</h2>
            <div className='block-all-documentation'>
                <div className='container-documentation-btn'>
                    <a className='btn-download btn-add' onClick={handleUploadClick}>
                        <img src={iconAdd} alt=''/>
                        Загрузить
                    </a>
                    <a className='container-list-btn'>
                        Загруженные
                    </a>
                </div>
                <div className='list-documentation'>
                    <SeachForDocumentation />
                </div>
            </div>
        </section>
    );
};

export default WorkDocumentation;