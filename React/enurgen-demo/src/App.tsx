import React, { useState, useEffect, useRef } from 'react'
import { getFileNames } from './Api'
import { CSVImage } from './CSVImage'
import './App.css'

const serverURL = 'http://localhost:5001/files'

function App() {
    const [fileNames, setFileNames] = useState<string[]>([])
    const fileInputRef = useRef<HTMLInputElement>(null)

    // Gets file names on initial load, assuming a database exists
    useEffect(() => {
        getFileNames(serverURL).then((fileNames) => setFileNames(fileNames))
    }, [])
    
    const selectFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            const selectedFiles = e.target.files
            const formData = new FormData()
            Array.from(selectedFiles).forEach((selectedFile) => {
                formData.append('data', selectedFile)
            })
            

            try {
                const response = await fetch(serverURL, {
                    method: 'POST',
                    body: formData
                })

                const currentFiles = await response.json()

                setFileNames(currentFiles['fileNames'])
            } catch (err) {
                console.log(err)
            }
        }
    }

    return (
    <>
        <div className='main'>
            <div className='sidebar'>
                    <div style={{justifyContent: 'center', fontWeight: 'bold', color: 'black'}}>
                        Files
                    </div>
                    <li className='fileList'>
                        {fileNames.map((name) => {return <ul key={name} className='listElement'>{name}</ul>})}
                    </li>
            </div>
            <div className='filenav'>
                <button
                    style={{position: 'absolute', right: '20px', top: '10px', marginTop: '5px', marginRight: '20px', width: 'px', height: '40px'}}
                    onClick={() => fileInputRef?.current && fileInputRef.current.click()}
                >
                    Browse...
                </button>
                <input 
                    style={{visibility: 'hidden'}}
                    id='file'
                    type='file'
                    onChange={selectFile}
                    accept=".csv"
                    multiple
                    ref={fileInputRef}
                />
                {fileNames.map((name) => {
                    return (
                        <div 
                            style={{display: 'grid', gridTemplateColumns:'100%', height: '75px', width: '140px', justifyItems: 'center'}}
                            key={name}
                        >
                            <CSVImage/>
                            {name}
                        </div>
                    )
                })}
            </div>
        </div>
    </>
    )
}

export default App
