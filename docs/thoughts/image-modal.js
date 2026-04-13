const zoomableFigures = document.querySelectorAll('.image-modal-trigger')

if (zoomableFigures.length > 0) {
  const modal = document.createElement('div')
  modal.className = 'image-modal'
  modal.hidden = true
  modal.innerHTML = `
    <figure class="image-modal-content">
      <button type="button" class="image-modal-close" aria-label="Close image preview">×</button>
      <img alt="">
      <figcaption hidden></figcaption>
    </figure>
  `

  const modalContent = modal.querySelector('.image-modal-content')
  const modalImage = modal.querySelector('img')
  const modalCaption = modal.querySelector('figcaption')
  const closeButton = modal.querySelector('.image-modal-close')

  const closeModal = () => {
    modal.hidden = true
    document.body.classList.remove('image-modal-open')
  }

  const openModal = () => {
    modal.hidden = false
    document.body.classList.add('image-modal-open')
  }

  closeButton.addEventListener('click', closeModal)
  modal.addEventListener('click', (event) => {
    if (event.target === modal) {
      closeModal()
    }
  })
  modalContent.addEventListener('click', (event) => {
    event.stopPropagation()
  })
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !modal.hidden) {
      closeModal()
    }
  })

  document.body.appendChild(modal)

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

      openModal()
    })
  })
}
