import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
        <div className='main'>
            <div className='sidebar'>
                <p>Files</p>
            </div>
            <div className='filenav'>
                SomeFiles
            </div>
        </div>
    </>
  )
}

export default App
