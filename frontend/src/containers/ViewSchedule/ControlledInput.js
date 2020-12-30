import React from 'react';
import ReactDOM from 'react-dom';
import styled from 'styled-components';

import AutosizeInput from 'react-input-autosize';

import editImg from 'assets/Edit.png';

class ControlledInput extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      title: props.name ? props.name : 'Untitled',
    };
  }

  submit() {
    let { title } = this.state;
    if (title.length === 0) {
      title = 'Untitled';
    }
    this.setState({
      title,
      editing: false,
    });
    // TODO: PATCH the schedule with new name=this.state.title
    this.props.rename(this.props.slug, title);
  }

  changeScheduleName(action) {
    const node = ReactDOM.findDOMNode(this);
    const child = node.querySelector("input[name='form-field-schedule-name']");
    if (action === 'focus') {
      child.focus();
    } else {
      child.blur();
    }
  }

  render() {
    return (
      <Container>
        {/* TODO: Disable spellcheck */}
        <AutosizeInput
          name="form-field-schedule-name"
          value={this.state.title}
          maxLength="20"
          onChange={(event) => {
            this.setState({
              title: event.target.value,
            });
          }}
          onFocus={() => {
            this.setState({
              editing: true,
            });
          }}
          onBlur={() => {
            this.submit();
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              this.changeScheduleName('blur');
            }
          }}
          inputStyle={{ fontSize: 32, backgroundColor: '#1a1a1a', border: 'none' }}
        />
        <button
          className={this.state.editing ? 'hide' : ''}
          onClick={() => {
            this.changeScheduleName('focus');
          }}
        >
          <img
            src={editImg}
            alt="Edit"
            style={{ width: 32, height: 32, marginLeft: 8 }}
          />
        </button>
      </Container>
    );
  }
}

const Container = styled.div`
  display: flex;
  align-items: center;
  color: white;
  background-color: #1a1a1a;

`;
export default ControlledInput;
