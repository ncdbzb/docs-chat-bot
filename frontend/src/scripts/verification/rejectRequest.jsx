const apiUrl = process.env.REACT_APP_API_URL;

export const RejectRequest = async (id, setFlagReject, setMessage) => {
    try {
        const response = await fetch(`${apiUrl}/admin/reject`, {
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
            setMessage('Заявка на верификацию отклонена!');
            setFlagReject(true);
        }
    } catch (error) {
        console.error("Error fetching user data:", error);
    }
};
