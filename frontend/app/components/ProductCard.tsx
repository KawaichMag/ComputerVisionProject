import './ProductCard.css'

type ProductCardProps = {
    name: string,
    cal: number,
    weight: number
}

function ProductCard(props: ProductCardProps) {
  return (
    <div className="prod-card">
        <span className="prod-name">
            {props.name}
        </span>
        <span className="prod-cal">
            {props.cal}
            <span className='prod-unit'>cal</span>
        </span>
        
        <span className="prod-weight">
            {props.weight}
            <span className='prod-unit'>g</span>
        </span>
        
        
    </div>
  )
}

export default ProductCard

