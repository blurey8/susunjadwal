import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import Helmet from 'react-helmet';
import { useSelector, useDispatch } from 'react-redux';

import { getSchedule, postRenameSchedule } from 'services/api';
import { makeAtLeastMs } from 'utils/promise';
import { setLoading } from 'redux/modules/appState';

import { decodeHtmlEntity } from 'utils/string';
import Schedule from './Schedule';
import ControlledInput from './ControlledInput';

function ViewSchedule({ match }) {
  const dispatch = useDispatch();
  const isMobile = useSelector((state) => state.appState.isMobile);
  const auth = useSelector((state) => state.auth);

  const [schedule, setSchedule] = useState(null);

  async function onRename(slug, value) {
    if (auth) {
      await postRenameSchedule(auth.userId, slug, value);
      setSchedule({ ...schedule, name: value });
    }
  }

  useEffect(() => {
    async function fetchSchedule() {
      dispatch(setLoading(true));
      const {
        data: { user_schedule },
      } = await makeAtLeastMs(getSchedule(match.params.scheduleId), 1000);
      setSchedule(user_schedule);
      dispatch(setLoading(false));
    }
    fetchSchedule();
  }, [match, dispatch]);

  const scheduleName = schedule && schedule.name;

  return (
    <>
      <Helmet
        title={scheduleName ? `Jadwal ${scheduleName}` : 'Memuat jadwal ...'}
        meta={[{ name: 'description', content: 'Description of Jadwal' }]}
      />

      {schedule && (
        <Container>
          {schedule.has_edit_access ? (
            <ControlledInput
              name={decodeHtmlEntity(schedule.name)}
              slug={match.params.scheduleId}
              rename={onRename}
            />
          ) : (
            <ScheduleName>
              {decodeHtmlEntity(schedule.name)}
            </ScheduleName>
          )}
        </Container>
      )}

      <Schedule
        width="100%"
        pxPerMinute={isMobile ? 0.7 : 0.9}
        schedule={schedule}
        startHour={7}
        endHour={21}
        showHeader
        showLabel
        showRoom
      />
    </>
  );
}

const Container = styled.div`
  padding: 32px 48px;
  padding-bottom: 16px;
  background-color: #1a1a1a;
`;

const ScheduleName = styled.div`
  font-size: 32px;
  color: white;
`;

export default ViewSchedule;
