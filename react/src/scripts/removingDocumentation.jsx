const apiUrl = process.env.REACT_APP_API_URL;

export const RemovingDocumentation = async (doc_name) => {
    try {
        const response = await fetch(`${apiUrl}/docks/delete-my?doc_name=${doc_name}`, {
            method: "DELETE",
            credentials: "include",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        window.location.reload();

    } catch (error) {
        console.error("Error fetching user data:", error);
    } finally {
        
    }
    return null;
};