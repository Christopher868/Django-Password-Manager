// Retrieves user's profile data
export async function getStoredProfileData(){
    try{
        const response = await fetch('/api/retrieve-profile/');

        if(!response.ok){
            throw new Error(`Http error! status: ${response.status}`)
        }
        const data = await response.json();
        return data

    } catch (err) {
        console.error(`Error retrieving user's profile data: ${err}`)
    }
}
