export const getFileNames = async (serverURL: string): Promise<string[]> => {
    const response = await fetch(serverURL, {
        method: 'GET'
    })

    const currentFiles = await response.json()

    return currentFiles['fileNames']
}
