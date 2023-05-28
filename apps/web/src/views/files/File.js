import {
  CButton,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CContainer,
  CForm,
  CFormInput,
  CFormSelect,
  CProgress,
  CProgressBar,
  CRow,
} from '@coreui/react'
import { createRef, useEffect, useState } from 'react'
import DataTable from 'react-data-table-component'
import API from 'src/utils/Api'

const Work = () => {
  const [items, setItems] = useState([])
  const [progress, setProgress] = useState(1)
  const [progressVisible, setProgressVisible] = useState('invisible')
  const [fileTypes, setFileTypes] = useState([])
  const [currentFileType, setCurrenFileType] = useState('building')
  const [totalRows, setTotalRows] = useState(0)
  const [limit, setLimit] = useState(10)

  const fileInput = createRef()

  const files_get_list = async (offset = 1) => {
    console.log(offset)
    const response = await API.get(`/files/?offset=${(offset - 1) * limit}&limit=${limit}`)
    setItems(response.data)
  }

  const files_get_types = async () => {
    const response = await API.get('/files/file_type/')
    const map_label = {
      building: 'Строения и основные справочники (Файл №1)',
      incident: 'Инциденты (Файл №2)',
      work: 'Исторические данные по работам (Файл №3)',
      work_type_kr: 'Виды работ (КР) (Файл №4)',
      work_type: 'Виды работ (обслуживание) (Файл №4)',
      event: 'Источники и возможные события (Файл №5)',
    }
    setFileTypes(
      response.data.map((elem) => {
        return { label: map_label[elem], value: elem }
      }),
    )
  }

  const files_get_count = async () => {
    const response = await API.get('/files/count/')
    setTotalRows(response.data)
  }

  const file_do = async (id) => {
    await API.get(`/files/${id}/do`)
  }

  const file_delete = async (id) => {
    await API.delete(`/files/${id}`)
    await files_get_list()
  }

  const onLoadFile = async (e) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget.form)
    formData.append('file', fileInput.current.files[0])
    setProgressVisible('visible')
    await API.post(`/files/?file_type=${currentFileType}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (data) => {
        setProgress(Math.round((100 * data.loaded) / data.total))
        console.log(progress)
      },
    })
    setProgressVisible('invisible')
    setProgress(1)
  }

  const Buttons = ({ id }) => {
    return (
      <>
        <CButton
          onClick={() => file_do(id)}
          size="sm"
          color="success"
          variant="outline"
          className="m-1"
        >
          Загрузить в БД
        </CButton>
        <CButton
          onClick={() => file_delete(id)}
          size="sm"
          color="danger"
          variant="outline"
          className="m-1"
        >
          <cilDelete /> Удалить
        </CButton>
      </>
    )
  }

  const columns = [
    {
      name: '#',
      selector: (row) => row.id,
      maxWidth: '50px',
      minWidth: '15px',
    },
    {
      name: 'Название',
      selector: (row) => row.name,
      wrap: 1,
      sortable: 1,
      minWidth: '400px',
    },
    {
      name: 'Тип файла',
      selector: (row) => row.file_type,
      wrap: 1,
      sortable: 1,
      maxWidth: '100px',
    },
    {
      name: 'Статус',
      selector: (row) => row.status,
      maxWidth: '100px',
    },
    {
      name: 'Действия',
      button: true,
      cell: (row) => <Buttons id={row.id} />,
      minWidth: '300px',
    },
  ]

  useEffect(() => {
    files_get_list()
    files_get_types()
    files_get_count()
  }, [progressVisible, limit])

  return (
    <CCard>
      <CCardHeader>
        <CContainer>
          <CRow>
            <CCol xs lg={10}>
              <h4>Источники данных: Файлы</h4>
            </CCol>
            <CCol xs lg={2}>
              <CForm>
                <CFormSelect
                  options={[...fileTypes]}
                  size="sm"
                  className="mb-2"
                  value={currentFileType}
                  onChange={(event) => setCurrenFileType(event.target.value)}
                />
                <CFormInput
                  type="file"
                  style={{ display: 'none' }}
                  ref={fileInput}
                  accept=".xls, .xlsx"
                  onChange={onLoadFile}
                />
                <CButton
                  size="sm"
                  color="primary"
                  variant="outline"
                  className="m-1 align-right w-100"
                  onClick={() => fileInput.current.click()}
                >
                  Добавить файл
                </CButton>
                {/* <CButton type="submit" style={{ display: 'none' }} ref={formSubmit}></CButton> */}
              </CForm>
            </CCol>
          </CRow>
          <CRow className="p-2">
            <CProgress height={3} className={progressVisible}>
              <CProgressBar value={progress} color="info" variant="striped" animated />
            </CProgress>
          </CRow>
        </CContainer>
      </CCardHeader>
      <CCardBody>
        <DataTable
          // className="rounded-4"
          columns={columns}
          data={items}
          direction="auto"
          fixedHeaderScrollHeight="300px"
          pagination
          paginationServer
          responsive
          subHeaderAlign="right"
          subHeaderWrap
          paginationTotalRows={totalRows}
          onChangePage={(offset) => {
            files_get_list(offset)
          }}
          onChangeRowsPerPage={(newPerPage, page) => {
            setLimit(newPerPage)
          }}
        />
      </CCardBody>
    </CCard>
  )
}
export default Work
