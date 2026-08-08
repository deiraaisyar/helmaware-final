'use client';

import Link from 'next/link';
import { Menu, X } from 'lucide-react';
import { useState } from 'react';
import Container from '@/components/common/Container';

interface NavbarProps {
    locale: string;
    dict: {
        about: string;
        projects: string;
        experience: string;
        skills: string;
        contact: string;
    };
}

export default function Navbar({ locale, dict }: NavbarProps) {
    const [isOpen, setIsOpen] = useState(false);

    const navItems =
        locale === 'id'
            ? [
                { label: 'Tentang', href: '#about' },
                { label: 'Proyek IT', href: '#projects' },
                { label: 'Proyek Non-IT', href: '#non-it-projects' },
                { label: 'Pengalaman', href: '#experience' },
                { label: 'Kontak', href: '#contact' },
            ]
            : [
                { label: 'About', href: '#about' },
                { label: 'IT Projects', href: '#projects' },
                { label: 'Non-IT Projects', href: '#non-it-projects' },
                { label: 'Experience', href: '#experience' },
                { label: 'Contact', href: '#contact' },
            ];

    return (
        <header className="sticky top-0 z-50 border-b border-[#E7E2DA] bg-[#F8F7F4]/80 backdrop-blur-md">
            <Container className="flex h-18 items-center justify-between">
                <Link
                    href={`/${locale}`}
                    className="text-xl font-semibold tracking-tight text-[#1F2937]"
                >
                    Regina Joan
                </Link>

                <div className="hidden items-center gap-8 md:flex">
                    {navItems.map((item) => (
                        <a
                            key={item.label}
                            href={`/${locale}${item.href}`}
                            className="relative text-sm font-medium text-[#1F2937] transition hover:text-[#C56E3D] after:absolute after:-bottom-2 after:left-0 after:h-[2px] after:w-0 after:bg-[#C56E3D] after:transition-all hover:after:w-full"
                        >
                            {item.label}
                        </a>
                    ))}

                    <div className="flex items-center rounded-full border border-[#E7E2DA] p-1">
                        <Link
                            href="/en"
                            className={`rounded-full px-3 py-1 text-xs ${locale === 'en'
                                ? 'bg-[#1F2937] text-white'
                                : 'text-[#1F2937]'
                                }`}
                        >
                            EN
                        </Link>

                        <Link
                            href="/id"
                            className={`rounded-full px-3 py-1 text-xs ${locale === 'id'
                                ? 'bg-[#1F2937] text-white'
                                : 'text-[#1F2937]'
                                }`}
                        >
                            ID
                        </Link>
                    </div>
                </div>

                <button
                    className="md:hidden"
                    onClick={() => setIsOpen(!isOpen)}
                    aria-label="Toggle menu"
                >
                    {isOpen ? <X size={24} /> : <Menu size={24} />}
                </button>
            </Container>

            {isOpen && (
                <div className="border-t border-[#E7E2DA] bg-[#F8F7F4] md:hidden">
                    <Container className="flex flex-col py-4">
                        {navItems.map((item) => (
                            <a
                                key={item.label}
                                href={`/${locale}${item.href}`}
                                className="py-3 text-sm font-medium text-[#1F2937]"
                                onClick={() => setIsOpen(false)}
                            >
                                {item.label}
                            </a>
                        ))}

                        <div className="mt-4 flex gap-2">
                            <Link
                                href="/en"
                                className={`rounded-full px-3 py-1 text-xs ${locale === 'en'
                                    ? 'bg-[#1F2937] text-white'
                                    : 'border border-[#E7E2DA] text-[#1F2937]'
                                    }`}
                            >
                                EN
                            </Link>

                            <Link
                                href="/id"
                                className={`rounded-full px-3 py-1 text-xs ${locale === 'id'
                                    ? 'bg-[#1F2937] text-white'
                                    : 'border border-[#E7E2DA] text-[#1F2937]'
                                    }`}
                            >
                                ID
                            </Link>
                        </div>
                    </Container>
                </div>
            )}
        </header>
    );
}
