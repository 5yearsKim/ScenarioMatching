import React, {useState, useEffect, useRef} from 'react';

export default function TypeWriter({text, delay=30 }) {
  const index = useRef(0);
  const [currentText, setCurrentText] = useState('');

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      setCurrentText((value) => value + text.charAt(index.current));
      index.current += 1;
    }, delay);
    return () => {
      clearTimeout(timeoutId);
    };
  }, [currentText, text]);

  useEffect(() => {
    setCurrentText('');
    index.current = 0;
  }, [text]);
  return <span>{currentText}</span>;
}