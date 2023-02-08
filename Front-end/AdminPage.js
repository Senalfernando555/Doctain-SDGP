function animateValue(el, start = 0, end = 0, is_price = false, duration = 1600) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;

    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    el.innerHTML = is_price
      ? prettyPrice(Math.floor(progress * (end - start) + start))
      : prettyNum(Math.floor(progress * (end - start) + start))

    // if not at end, continue
    // if at end, return final number WITHOUT math operation to preserve decimals
    if (progress < 1) window.requestAnimationFrame(step);
    else el.innerHTML = is_price
      ? this.prettyPrice(end)
      : this.prettyNum(end)
  };
  window.requestAnimationFrame(step);
}

function prettyNum(value = 0) {
  return value.toLocaleString('en-US');	
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.count-up').forEach(el => {
    animateValue(el, 0, el.dataset.value, el.dataset.isPrice);
  })
})
