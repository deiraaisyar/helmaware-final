import Link from 'next/link';
import Container from '@/components/common/Container';

interface FooterProps {
    locale: string;
}

export default function Footer({ locale }: FooterProps) {
    const isID = locale === 'id';

    return (<footer className="border-t border-[#E7E2DA] bg-[#F8F7F4]"> <Container className="flex flex-col items-center justify-between gap-4 py-8 text-sm text-[#6B7280] md:flex-row"> <div> <p className="font-medium text-[#1F2937]">Regina Joan</p> <p className="mt-1 max-w-md">
        {isID
            ? 'Mahasiswa Ilmu Komputer yang berfokus pada software engineering, AI, product development, dan teknologi yang berdampak bagi komunitas.'
            : 'Computer Science student passionate about software engineering, AI, product development, and community-driven technology.'} </p> </div>
        <div className="flex flex-wrap items-center gap-6">
            <Link href={`/${locale}#about`} className="transition hover:text-[#C56E3D]">
                {isID ? 'Tentang' : 'About'}
            </Link>
            <Link href={`/${locale}#projects`} className="transition hover:text-[#C56E3D]">
                {isID ? 'Proyek' : 'Projects'}
            </Link>
            <Link href={`/${locale}#experience`} className="transition hover:text-[#C56E3D]">
                {isID ? 'Pengalaman' : 'Experience'}
            </Link>
            <Link href={`/${locale}#contact`} className="transition hover:text-[#C56E3D]">
                {isID ? 'Kontak' : 'Contact'}
            </Link>
        </div>
    </Container>

        <Container className="border-t border-[#E7E2DA] py-4 text-center text-xs text-[#9CA3AF]">
            © 2026 Regina Joan. {isID ? 'Seluruh hak cipta dilindungi.' : 'All rights reserved.'}
        </Container>
    </footer>
    );
}
