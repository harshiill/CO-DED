'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  IconHome,
  IconLayoutDashboard,
  IconSeo,
  IconEdit,
  IconDatabasePlus,
} from '@tabler/icons-react';
import { Code, Group } from '@mantine/core';
import classes from './navbarminimal.module.css';
import { ActionToggle } from '../darkmode/ActionToggle';

const data = [
  { link: '/', label: 'Home', icon: IconHome },
  { link: '/dashboard', label: 'Dashboard', icon: IconLayoutDashboard },
  { link: '/seo_', label: 'SEO Optimization', icon: IconSeo },
  { link: '/updatecontent', label: 'Content Update', icon: IconEdit },
  { link: '/content_add', label: 'Content Add', icon: IconDatabasePlus },
  { link: '/broken_links', label: 'Broken Link Provider', icon: IconDatabasePlus },
];

export function NavbarMinimal() {
  // Get current pathname from Next.js router
  const pathname = usePathname();

  // Use <Link> instead of <a> to enable client-side navigation
  const links = data.map((item) => (
    <Link
      key={item.label}
      href={item.link}
      className={`${classes.link} ${pathname === item.link ? classes.active : ''}`}
    >
      <item.icon className={classes.linkIcon} stroke={1.5} />
      <span>{item.label}</span>
    </Link>
  ));

  return (
    <nav className={classes.navbar}>
      <div className={classes.navbarMain}>
        <Group className={classes.header} justify="space-between">
          <Code fw={700}>v3.1.2</Code>
        </Group>
        {links}
      </div>
      <div>
        <ActionToggle />
      </div>
    </nav>
  );
}
