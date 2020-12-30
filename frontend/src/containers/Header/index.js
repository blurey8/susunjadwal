import React, { useState } from 'react';
import styled, { createGlobalStyle } from 'styled-components';
import { useSelector } from 'react-redux';

import { Link, NavLink } from 'react-router-dom';
import { slide as Menu } from 'react-burger-menu';

import './styles.css';

const HideBodyOverflow = createGlobalStyle`
  body {
    overflow: hidden;
  }
`;

const LINKS = [
  { to: '/susun', label: 'Buat Jadwal' },
  { to: '/jadwal', label: 'Daftar Jadwal' },
  { to: '/logout', label: 'Logout' },
];

function renderHeaderLink() {
  return (
    <>
      {LINKS.map(({ to, label }) => (
        <HeaderLink key={to} to={to}>
          {label}
        </HeaderLink>
      )).reverse()}
    </>
  );
}

function Header() {
  const isMobile = useSelector((state) => state.appState.isMobile);
  const [isOpened, setOpen] = useState(false);
  const auth = useSelector((state) => state.auth);

  function toggleMenu() {
    setOpen(!isOpened);
  }

  // JSX code for menu and the checking for isMobile are included to a variable named menuPage

  const menuPage = isMobile ? (
    <Menu
      isOpen={isOpened}
      burgerButtonClassName="menu"
      right
      onStateChange={({ isOpen }) => setOpen(isOpen)}
      styles={{
        bmMenuWrap: {
          height: 'calc(100vh - 64px)',
        },
        bmItemList: {
          height: 'none',
        },
      }}
    >
      {isOpened && <HideBodyOverflow />}
      {LINKS.map(({ to, label }) => (
        <MenuLink key={to} to={to} onClick={toggleMenu}>
          {label}
        </MenuLink>
      ))}
    </Menu>
  ) : (
    renderHeaderLink()
  );

  return (
    <Container>
      <LogoLink to="/">
        <h1>
          Susun
          <span>Jadwal</span>
        </h1>
      </LogoLink>
      {auth ? menuPage : null}
    </Container>
  );
  // The checking above is added for auth only
}

export default Header;

const Container = styled.div`
  width: 100%;
  height: 64px;
  padding: 0.5rem 0 0.5rem 0;
  background-color: #333333;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  z-index: 5;
  position: fixed;
  a {
    color: white;
  }

  a:hover {
    color: #828282;
  }

  a.active {
    color: #F2994A !important;
  }
`;

const MenuLink = styled(NavLink)`
  font-weight: 700;
  color: #fff;
  margin-right: 2rem;
`;

const HeaderLink = styled(NavLink)`
  float: right;
  line-height: 3rem;
  font-weight: 700;
  color: #222222;
  margin-right: 2rem;
`;

const LogoLink = styled(Link)`
  h1 {
    margin: 0 0 0 ${(props) => (props.theme.mobile ? '1rem' : '3rem')};
    line-height: 3rem;
    font-size: 2rem;
    font-weight: 700;
    display: inline-block;
    color: #ffffff;

    span {
      color: #F2994A;
    }
  }
`;
