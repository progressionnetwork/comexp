import {
  CBadge,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CContainer,
  CListGroup,
  CListGroupItem,
  CNav,
  CNavItem,
  CNavLink,
  CRow,
  CTabContent,
  CTabPane,
} from '@coreui/react'
import { useEffect, useState } from 'react'
import DataTable from 'react-data-table-component'
import { Map, Placemark, YMaps } from 'react-yandex-maps'
import API from 'src/utils/Api'

const BuildingSubRow = (data) => {
  return (
    <CListGroup>
      {data.data.events.map((elem) => (
        <CListGroupItem component="button" key={elem.id}>
          <CBadge>{elem.date_close}</CBadge> {elem.name}
        </CListGroupItem>
      ))}
    </CListGroup>
  )
}

const BuildingOnMaps = ({ address }) => {
  const [mapCenter, setMapCenter] = useState({ center: [55.75, 37.57], zoom: 18 })
  const [point, setPoint] = useState([55.75, 37.57])
  const YM_TOKEN = process.env.REACT_APP_YM_TOKEN
  const geocode = async (ymaps) => {
    const geoObj = await ymaps.geocode(`г. Москва, ${address}`)
    setMapCenter({ center: geoObj.geoObjects.get(0).geometry.getCoordinates(), zoom: 18 })
    setPoint(geoObj.geoObjects.get(0).geometry.getCoordinates())
    console.log(mapCenter)
  }
  return (
    <YMaps
      query={{
        ns: 'use-load-option',
        apikey: YM_TOKEN,
        load: 'geocode',
      }}
      on
    >
      <div>
        <Map state={mapCenter} style={{ width: '100%', height: '400px' }} onLoad={geocode}>
          <Placemark geometry={point} />
        </Map>
      </div>
    </YMaps>
  )
}

const BuildingInfo = (data) => {
  const [activeKey, setActiveKey] = useState(1)

  return (
    <>
      <CNav variant="tabs" role="tablist">
        <CNavItem>
          <CNavLink
            active={activeKey === 1}
            onClick={() => setActiveKey(1)}
            style={{ cursor: 'pointer' }}
          >
            Информация
          </CNavLink>
        </CNavItem>
        <CNavItem>
          <CNavLink
            active={activeKey === 2}
            onClick={() => setActiveKey(2)}
            style={{ cursor: 'pointer' }}
          >
            Инциденты
          </CNavLink>
        </CNavItem>
        <CNavItem>
          <CNavLink
            active={activeKey === 3}
            onClick={() => setActiveKey(3)}
            style={{ cursor: 'pointer' }}
          >
            История работ
          </CNavLink>
        </CNavItem>
        <CNavItem>
          <CNavLink
            active={activeKey === 4}
            onClick={() => setActiveKey(4)}
            style={{ cursor: 'pointer' }}
          >
            На карте
          </CNavLink>
        </CNavItem>
      </CNav>
      <CTabContent>
        <CTabPane role="tabpanel" aria-labelledby="home-tab" visible={activeKey === 1}>
          <CContainer fluid>
            <CRow xs={{ cols: 1 }} sm={{ cols: 1 }} md={{ cols: 2 }}>
              <CCol>
                <CCard className="m-2">
                  <CCardHeader>Общая информация </CCardHeader>
                  <CCardBody>
                    <div style={{ fontSize: '0.8rem' }}>
                      Проект: {data.data.project_series ? data.data.project_series.name : '-'}
                    </div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Аварийность:
                      {data.data.attribute_crash ? data.data.attribute_crash.name : '-'}
                    </div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Статус управления МКД:
                      {data.data.status_manage_mkd ? data.data.status_manage_mkd.name : '-'}
                    </div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Статус МКД:
                      {data.data.status_mkd ? data.data.status_mkd.name : '-'}
                    </div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Категория МКД:
                      {data.data.category_mkd ? data.data.category_mkd.name : '-'}
                    </div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Тип жилищного фонда:
                      {data.data.type_building_fund ? data.data.type_building_fund.name : '-'}
                    </div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Вид социального объекта:
                      {data.data.type_social_object ? data.data.type_social_object.name : '-'}
                    </div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Количество этажей: {data.data.count_floor}
                    </div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Количество подъездов: {data.data.count_entrance}
                    </div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Количество квартир: {data.data.count_apartment}
                    </div>
                  </CCardBody>
                </CCard>
              </CCol>
              <CCol>
                <CCard className="m-2">
                  <CCardHeader>Лифты </CCardHeader>
                  <CCardBody>
                    <div style={{ fontSize: '0.8rem' }}>
                      Количество пассажирских лифтов: {data.data.count_elevator_passenger}
                    </div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Количество грузовых лифтов: {data.data.count_elevator_cargo}
                    </div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Количество грузо-пассажирских лифтов:
                      {data.data.count_elevator_cargopassenger}
                    </div>
                  </CCardBody>
                </CCard>
              </CCol>
              <CCol>
                <CCard className="m-2">
                  <CCardHeader>Площадь </CCardHeader>
                  <CCardBody>
                    <div style={{ fontSize: '0.8rem' }}>Общая: {data.data.total_area}</div>
                    <div style={{ fontSize: '0.8rem' }}>Жилая: {data.data.total_living_area}</div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Нежилая: {data.data.total_nonliving_area}
                    </div>
                  </CCardBody>
                </CCard>
              </CCol>
              <CCol>
                <CCard className="m-2">
                  <CCardHeader>Материалы </CCardHeader>
                  <CCardBody>
                    <div style={{ fontSize: '0.8rem' }}>
                      Стены: {data.data.wall_material ? data.data.wall_material.name : '- '}
                    </div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Кровля: {data.data.roof_material ? data.data.roof_material.name : '-'}
                    </div>
                    <div style={{ fontSize: '0.8rem' }}>
                      Очередность уборки кровли:
                      {data.data.queue_clean ? data.data.queue_clean.name : '-'}
                    </div>
                  </CCardBody>
                </CCard>
              </CCol>
            </CRow>
          </CContainer>
        </CTabPane>
        <CTabPane role="tabpanel" aria-labelledby="profile-tab" visible={activeKey === 2}>
          {data.data.incidents && (
            <CListGroup>
              {data.data.incidents.map((elem) => (
                <CListGroupItem component="button" key={elem.id}>
                  {elem.date_close && (
                    <CBadge color="success" className="m-2">
                      {elem.date_close}
                    </CBadge>
                  )}
                  {!elem.date_close && (
                    <CBadge color="danger" className="m-2">
                      Не закрыто
                    </CBadge>
                  )}
                  {elem.event.name}
                </CListGroupItem>
              ))}
            </CListGroup>
          )}
          {data.data.incidents.length === 0 && (
            <div className="m-3">Инцидентов по данному объекту не обнаружено</div>
          )}
        </CTabPane>
        <CTabPane role="tabpanel" aria-labelledby="contact-tab" visible={activeKey === 3}>
          {data.data.works && (
            <CListGroup>
              {data.data.works.map((elem) => (
                <CListGroupItem component="button" key={elem.id}>
                  {elem.fact_date_end && (
                    <CBadge color="success" className="m-2">
                      {elem.fact_date_end}
                    </CBadge>
                  )}
                  {!elem.fact_date_end && (
                    <CBadge color="danger" className="m-2">
                      Не выполнено
                    </CBadge>
                  )}
                  {elem.work_type.name}
                </CListGroupItem>
              ))}
            </CListGroup>
          )}
          {data.data.works.length === 0 && (
            <div className="m-3">Работ по данному объекту не обнаружено</div>
          )}
        </CTabPane>
        <CTabPane role="tabpanel" aria-labelledby="contact-tab" visible={activeKey === 4}>
          <BuildingOnMaps address={data.data.name} />
        </CTabPane>
      </CTabContent>
    </>
  )
}

const Building = () => {
  const [items, setItems] = useState([])
  const [totalRows, setTotalRows] = useState(0)
  const [limit, setLimit] = useState(10)

  const endpoint = '/building/'

  const get_list = async (offset = 1) => {
    const response = await API.get(`${endpoint}?offset=${(offset - 1) * limit}&limit=${limit}`)
    console.log(response.data)
    setItems(response.data)
  }

  const get_count = async () => {
    const response = await API.get(`${endpoint}count/`)
    setTotalRows(response.data)
  }

  const columns = [
    {
      name: '#',
      selector: (row) => row.id,
      maxWidth: '100px',
    },
    {
      name: 'Адрес',
      selector: (row) => row.name,
      wrap: 1,
    },
  ]

  useEffect(() => {
    get_list()
    get_count()
  }, [limit])

  return (
    <CCard>
      <CCardHeader>
        <h4>Строения</h4>
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
            get_list(offset)
          }}
          onChangeRowsPerPage={(newPerPage, page) => {
            setLimit(newPerPage)
          }}
          expandableRows={true}
          expandOnRowClicked={false}
          expandOnRowDoubleClicked={false}
          expandableRowsHideExpander={false}
          expandableRowsComponent={BuildingInfo}
        />
      </CCardBody>
    </CCard>
  )
}
export default Building
