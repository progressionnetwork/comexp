import {
  CButton,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CContainer,
  CForm,
  CListGroup,
  CListGroupItem,
  CRow,
} from '@coreui/react'
import { useEffect, useState } from 'react'
import DataTable from 'react-data-table-component'
import { EditInline } from 'src/components/EditInline'
import API from 'src/utils/Api'
const ExpandetComponent = (data) => {
  return (
    <CListGroup>
      {data.data.events.map((elem) => (
        <CListGroupItem key={elem.id}>
          <CContainer>
            <CRow>
              <CCol xs lg={10}>
                {elem.name}
              </CCol>
              <CCol xs lg={2}>
                <EditInline
                  value={elem.priority}
                  endPoint={`/event/${elem.id}`}
                  attr="priority"
                  floatNumber={6}
                />
              </CCol>
            </CRow>
          </CContainer>
        </CListGroupItem>
      ))}
    </CListGroup>
  )
}

const SourceEvent = () => {
  const [items, setItems] = useState([])
  const [totalRows, setTotalRows] = useState(0)
  const [limit, setLimit] = useState(10)

  const endpoint = '/sourcesystem'
  const title = 'Источники событий'

  const get_list = async (offset = 1) => {
    const response = await API.get(`${endpoint}/?offset=${(offset - 1) * limit}&limit=${limit}`)
    let sources = response.data
    sources.map((elem) => {
      elem.events.sort((a, b) => (a.priority < b.priority ? 1 : -1))
    })
    sources.sort((a, b) => (a.priority < b.priority ? 1 : -1))
    setItems(response.data)
  }

  const get_count = async () => {
    const response = await API.get(`${endpoint}/count/`)
    setTotalRows(response.data)
  }

  const handelUpdatePriority = async () => {
    await API.get('/event/update_priority/')
  }

  const columns = [
    {
      name: '#',
      selector: (row) => row.id,
      maxWidth: '100px',
    },
    {
      name: 'Наименование',
      selector: (row) => row.name,
    },
    {
      name: 'Приоритет',
      cell: (row) => (
        <EditInline value={row.priority} endPoint={`/sourcesystem/${row.id}`} attr="priority" />
      ),
      maxWidth: '200px',
      right: true,
    },
  ]

  useEffect(() => {
    get_list()
    get_count()
  }, [limit])

  return (
    <CCard>
      <CCardHeader>
        <CContainer>
          <CRow>
            <CCol xs lg={8}>
              <h4>{title}</h4>
            </CCol>
            <CCol xs lg={4}>
              <CForm>
                <CButton
                  size="sm"
                  color="success"
                  variant="outline"
                  className="m-1 align-right w-100"
                  onClick={handelUpdatePriority}
                >
                  Обновить приоритеты событий
                </CButton>
              </CForm>
            </CCol>
          </CRow>
        </CContainer>
      </CCardHeader>
      <CCardBody>
        <DataTable
          // className="rounded-4"
          columns={columns}
          data={items}
          direction="auto"
          expandableRows={true}
          expandOnRowClicked={false}
          expandOnRowDoubleClicked={false}
          expandableRowsHideExpander={false}
          expandableRowsComponent={ExpandetComponent}
          pagination
          paginationServer
          responsive
          subHeaderAlign="right"
          subHeaderWrap
          paginationTotalRows={totalRows}
          onChangePage={(offset) => {
            get_list(offset)
          }}
          onChangeRowsPerPage={(newPerPage, page) => {
            setLimit(newPerPage)
          }}
        />
      </CCardBody>
    </CCard>
  )
}
export default SourceEvent
