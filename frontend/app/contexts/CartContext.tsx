import {createContext, useState, useContext, useEffect } from 'react'

type ProductCardProps = {
    amount: number,
    name: string,
    cal: number,
    weight: number
}

type CartContextType = {
    cart: ProductCardProps[];
    setCart: React.Dispatch<React.SetStateAction<ProductCardProps[]>> | null;
};

export const CartContext = createContext<CartContextType>({
  cart: [],
  setCart: () => {}
});

type CartProviderProps = {
  children: React.ReactNode;
};

export default function ThemeProvider({ children }: CartProviderProps) {
  const [cart, setCart] = useState<ProductCardProps[]>([]);

  return (
    <CartContext.Provider value={{ cart, setCart }}>
      {children}
    </CartContext.Provider>
  );
}

export const useCart = () => useContext(CartContext)