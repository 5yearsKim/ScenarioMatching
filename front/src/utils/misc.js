
export function float2color( percentage ) {
  const toHex = (num) => {
    return Number(parseInt( num , 10)).toString(16);
  };
  percentage = Math.max(0, Math.min(1, percentage));
  var colorR = 254 - parseInt(60 * percentage);
  var colorG = 254 - parseInt(240* percentage);
  var colorB = 254 - parseInt(250* percentage);
  return '#' + toHex(colorR) + toHex(colorG) + toHex(colorB);
}

export function invertColor(color) {
  const hex = color.replace('#', '');
  return '#' + (Number(`0x1${hex}`) ^ 0xFFFFFF).toString(16).substr(1).toUpperCase();
}

export const highlightText = (text, matched_substring, start, end) => {
  const highlightTextStart = matched_substring.offset;
  const highlightTextEnd = highlightTextStart + matched_substring.length;

  const beforeText = text.slice(start, highlightTextStart);

  const highlightedText = text.slice(highlightTextStart, highlightTextEnd);

  const afterText = text.slice(highlightTextEnd, end || text.length);

  return [beforeText, `<strong>${highlightedText}</strong>`, afterText];
};


