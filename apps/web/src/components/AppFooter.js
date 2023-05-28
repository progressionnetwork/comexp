import { CFooter } from '@coreui/react'
import React from 'react'

const AppFooter = () => {
  return (
    <CFooter>
      <div>Команда &apos;Intellect Group&apos;, 2023 г.</div>
      <div className="ms-auto">
        <span className="me-1"></span>
        Сделано для Департамента ЖКХ г. Москвы
      </div>
    </CFooter>
  )
}

export default React.memo(AppFooter)
