import { Card, type CardProps } from '@mui/material'
import React from 'react'

interface CardsCollageProps {
    images: string[]
}

function CardsCollage( { images } : CardsCollageProps ) {
    return (
        <div className='cards-collage'
            style={{
                display: 'flex',
            }}
            >
            {images.map((item) => {
                return <img src={item}/>
            })}
        </div>
    )
}

type HistoryCardProps = CardProps & CardsCollageProps;

export default function HistoryCard( props : HistoryCardProps) {
  return (
    <Card>
      <CardsCollage images={props.images}/>
    </Card>
  )
}
