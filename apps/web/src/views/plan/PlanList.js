import {
  CBadge,
  CButton,
  CCard,
  CCardBody,
  CCardHeader,
  CListGroup,
  CListGroupItem,
} from '@coreui/react'
import { useEffect, useState } from 'react'
import 'react-datepicker/dist/react-datepicker.css'
import API from 'src/utils/Api'

const PlanList = () => {
  const [listPlan, setListPlan] = useState([])
  const get_plans = async () => {
    const response = await API.get(`plan/?offset=0&limit=100`)
    setListPlan(response.data)
  }
  useEffect(() => {
    get_plans()
    console.log(listPlan)
  }, [])

  const handleDelete = async (id) => {
    await API.delete(`/plan/${id}`)
    await get_plans()
  }
  const handleDownload = async (id) => {
    // const result = await API.get(`/plan/${id}/xlsx`)
    fetch(`${process.env.REACT_APP_API_URL}/plan/${id}/xlsx/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        Authorization: `Token ${localStorage.getItem('token')}`,
      },
    })
      .then((response) => response.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(new Blob([blob]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `export.xlsx`)

        // Append to html link element page
        document.body.appendChild(link)

        // Start download
        link.click()

        // Clean up and remove the link
        link.parentNode.removeChild(link)
      })
  }
  return (
    <CCard>
      <CCardHeader>
        <h4>Список планирования</h4>
      </CCardHeader>
      <CCardBody>
        <CListGroup>
          {listPlan &&
            listPlan.map((elem) => (
              <CListGroupItem
                key={elem.id}
                style={{ display: 'flex', justifyContent: 'space-between' }}
              >
                <div>
                  {elem.status === 1 && (
                    <CBadge color="success" className="m-1">
                      Готово
                    </CBadge>
                  )}
                  {elem.status === 0 && (
                    <CBadge color="warning" className="m-1">
                      В работе
                    </CBadge>
                  )}
                  <a href={`/#/plan/${elem.id}`}>{elem.name}</a>
                </div>
                <div>
                  <CButton
                    onClick={() => handleDownload(elem.id)}
                    size="sm"
                    color="success"
                    variant="outline"
                    className="m-1"
                  >
                    Скачать
                  </CButton>
                  <CButton
                    onClick={() => handleDelete(elem.id)}
                    size="sm"
                    color="danger"
                    variant="outline"
                    className="m-1"
                  >
                    Удалить
                  </CButton>
                </div>
              </CListGroupItem>
            ))}
        </CListGroup>
      </CCardBody>
    </CCard>
  )
}

export default PlanList
