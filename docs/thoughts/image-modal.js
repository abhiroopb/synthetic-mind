const zoomableFigures = document.querySelectorAll('.image-modal-trigger')

if (zoomableFigures.length > 0) {
  const dialog = document.createElement('dialog')
  dialog.className = 'image-modal'
  dialog.innerHTML = `
    <figure class="image-modal-content">
      <button type="button" class="image-modal-close" aria-label="Close image preview">×</button>
      <img alt="">
      <figcaption hidden></figcaption>
    </figure>
  `

  const modalImage = dialog.querySelector('img')
  const modalCaption = dialog.querySelector('figcaption')
  const closeButton = dialog.querySelector('.image-modal-close')

  const closeModal = () => {
    if (dialog.open) {
      dialog.close()
    }
  }

  closeButton.addEventListener('click', closeModal)
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) {
      closeModal()
    }
  })

  document.body.appendChild(dialog)

  zoomableFigures.forEach((trigger) => {
    const image = trigger.querySelector('img')
    const caption = trigger.closest('figure')?.querySelector('figcaption')?.textContent?.trim() || ''

    if (!image) {
      return
    }

    trigger.addEventListener('click', () => {
      modalImage.src = image.currentSrc || image.src
      modalImage.alt = image.alt

      if (caption) {
        modalCaption.hidden = false
        modalCaption.textContent = caption
      } else {
        modalCaption.hidden = true
        modalCaption.textContent = ''
      }

      dialog.showModal()
    })
  })
}
