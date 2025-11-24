import React, { useCallback, useMemo, useState } from 'react'
import './RecipeSearchPage.css'
import { useDropzone } from 'react-dropzone'
import PredictionCard from '~/components/PredictionCard';

const baseStyle = {
    width: '400px',
    height: '400px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    overflow: 'hidden',
    borderWidth: 2,
    borderRadius: '2em',
    borderColor: '#eeeeee',
    borderStyle: 'dashed',
    backgroundColor: 'transparent',
    outline: 'none',
    transition: 'border .24s ease-in-out',
    justifyContent: 'center'
  };

  const focusedStyle = {
    borderColor: '#2196f3'
  };

  const acceptStyle = {
    borderColor: '#00e676'
  };

  const rejectStyle = {
    borderColor: '#ff1744'
  };

export default function RecipeSearchPage() {
  const [image, setImage] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: any) => {
    acceptedFiles.forEach((file: any) => {
      const reader = new FileReader()

      reader.onabort = () => console.log('file reading was aborted')
      reader.onerror = () => console.log('file reading has failed')
      reader.onload = () => {
        const binaryStr = reader.result
        console.log(binaryStr)
        if (binaryStr) {
          const blob = new Blob([binaryStr], { type: 'image/jpeg' }); // Adjust MIME type if necessary
          const blobUrl = URL.createObjectURL(blob);
          setImage(blobUrl)
        }
      }
      reader.readAsArrayBuffer(file)
    })
  }, [])
  
  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isFocused,
    isDragAccept,
    isDragReject
  } = useDropzone({onDrop})

  const style = useMemo(() => ({
    ...baseStyle,
    ...(isFocused ? focusedStyle : {}),
    ...(isDragAccept ? acceptStyle : {}),
    ...(isDragReject ? rejectStyle : {})
  }), [
    isFocused,
    isDragAccept,
    isDragReject
  ]);
  
  // @ts-ignore
  return (
    <div className='recipesearchpage'>
      
      <div className="photo-load">
        <span className="photo-load-header">Your Photo Here</span>
        <div {...getRootProps({// @ts-ignore
         style})}>
          <input {...getInputProps()} />
          {
            !image? 
            isDragActive ?
              <p>Drop the files here ...</p> :
              <p>Drag 'n' drop some files here, or click to select files</p>
            :
            <img style={{width:"100%", height:"100%", objectFit:"cover"}} src={image} alt="" />
          }
        </div>
      </div>
      <div className="detected-conteiner">
        <span className="detected-container-header">
          <span>Amount</span><span>Name</span><span>Weight</span><span>Calories</span>
        </span>
        <div className="detected-conteiner-list">
          <PredictionCard name="broccoli" amount={1} weight={300} cal={105}/>
          <PredictionCard name="eggs" amount={2} weight={100} cal={140}/>
          <PredictionCard name="carrot" amount={1} weight={90} cal={37}/>
          <PredictionCard name="tomato" amount={1} weight={120} cal={22}/>
        </div>
      </div>
      <div className="current-chart">
          <span className="current-chart-header">
            Current Chart
          </span>
          <div className="current-chart-list">
            <PredictionCard name="cucumbers" amount={2} weight={80} cal={15}/>
            <PredictionCard name="tomatoes" amount={3} weight={210} cal={65}/>
            <PredictionCard name="onions" amount={1} weight={120} cal={45}/>
            <PredictionCard name="potatoes" amount={4} weight={600} cal={520}/>
            <PredictionCard name="chicken breast" amount={2} weight={300} cal={330}/>
            <PredictionCard name="cheddar cheese" amount={1} weight={90} cal={360}/>
            <PredictionCard name="olive oil" amount={1} weight={15} cal={120}/>
            <PredictionCard name="carrots" amount={5} weight={400} cal={165}/>
            <PredictionCard name="lettuce" amount={1} weight={200} cal={30}/>
            <PredictionCard name="avocado" amount={1} weight={160} cal={250}/>
            <PredictionCard name="salmon fillet" amount={1} weight={200} cal={410}/>
            <PredictionCard name="oats" amount={2} weight={160} cal={620}/>
            <PredictionCard name="banana" amount={2} weight={240} cal={210}/>
            <PredictionCard name="strawberries" amount={1} weight={150} cal={50}/>
            <PredictionCard name="pasta" amount={3} weight={360} cal={1240}/>
            <PredictionCard name="rice" amount={2} weight={300} cal={1040}/>
            <PredictionCard name="black beans" amount={1} weight={240} cal={315}/>
            <PredictionCard name="butter" amount={1} weight={50} cal={360}/>
            <PredictionCard name="yogurt" amount={1} weight={200} cal={125}/>
            <PredictionCard name="apple" amount={2} weight={300} cal={190}/>
          </div>
      </div>
  </div>
  )
}
