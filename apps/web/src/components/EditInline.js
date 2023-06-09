import { cilCheckAlt, cilPencil, cilX } from '@coreui/icons'
import CIcon from '@coreui/icons-react'
import { CBadge, CButton, CFormInput, CInputGroup } from '@coreui/react'
import { useState } from 'react'
import API from 'src/utils/Api'
export const EditInline = ({ value, endPoint, attr, floatNumber = 2 }) => {
  const [isEdit, setIsEdit] = useState(false)
  const [oldValue, setOldValue] = useState(value)
  const [newValue, setNewValue] = useState(oldValue)

  const handleOk = (event) => {
    setIsEdit(false)
    setOldValue(newValue)
    let data = {}
    data[attr] = Number(newValue)
    API.patch(endPoint, data)
    console.log(newValue)
  }

  const handleCancel = (event) => {
    setNewValue(oldValue)
    setIsEdit(false)
    console.log(newValue)
  }

  return (
    <CInputGroup className="mb-1" style={{ display: 'flex', justifyContent: 'end' }} size="sm">
      {!isEdit && (
        <>
          <h4 className="m-1">
            <CBadge
              style={{ display: 'flex', justifyContent: 'space-between', cursor: 'pointer' }}
              color={newValue > 0.8 ? 'danger' : newValue > 0.4 ? 'warning' : 'success'}
              onClick={() => {
                setIsEdit(true)
              }}
            >
              <div className="me-3">{Number(newValue).toFixed(floatNumber)}</div>
              <CIcon icon={cilPencil} />
            </CBadge>
          </h4>
        </>
      )}
      {isEdit && (
        <>
          <CFormInput
            placeholder="0.01"
            disabled={!isEdit}
            value={newValue}
            onChange={(event) => {
              setNewValue(event.target.value)
            }}
            style={{ maxWidth: '64px' }}
          />
          <CButton type="button" color="success" variant="outline" onClick={handleOk}>
            <CIcon icon={cilCheckAlt} />
          </CButton>
          <CButton type="button" color="danger" variant="outline" onClick={handleCancel}>
            <CIcon icon={cilX} />
          </CButton>
        </>
      )}
    </CInputGroup>
  )
}
