import { useState } from "react";

export const useRequestAddDocumentation = () => {
    const apiUrl = process.env.REACT_APP_API_URL;
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const sendRequest = async ({ docName, file, setFlag, setMessage }) => {
        try {
            const formDatas = new FormData();
            formDatas.append('file', file);

            const response = await fetch(`${apiUrl}/docks/add_data?doc_name=${docName}`, {
                method: 'POST',
                credentials: 'include',
                body: formDatas
            });


            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            setMessage('Документ успешно добавлен!');
            setFlag(true);
            setIsLoggedIn(true);
            return response.json();
        } catch (error) {
            console.error('Error fetching user data:', error);
            throw error;
        }
    };

    return { sendRequest, isLoggedIn };
};