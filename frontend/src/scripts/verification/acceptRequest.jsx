const apiUrl = process.env.REACT_APP_API_URL;

export const AcceptRequest = async ({ id, setFlagAccept, setMessage }) => {
    try {
        const response = await fetch(`${apiUrl}/admin/accept`, {
            method: "POST",
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ request_id: id }),
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        } else {
            setMessage('Заявка на верификацию одобрена!');
            setFlagAccept(true);
        }
    } catch (error) {
        console.error("Error fetching user data:", error);
    }
};
