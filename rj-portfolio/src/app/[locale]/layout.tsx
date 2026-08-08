import type { Metadata } from 'next';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';
import { getDictionary } from '@/lib/getDictionary';

export const metadata: Metadata = {
    title: 'Regina Joan | Portfolio',
    description: 'Computer Science student portfolio',
};

interface LocaleLayoutProps {
    children: React.ReactNode;
    params: Promise<{
        locale: string;
    }>;
}

export default async function LocaleLayout({
    children,
    params,
}: LocaleLayoutProps) {
    const { locale } = await params;
    const dict = await getDictionary(locale);

    return (
        <> <Navbar locale={locale} dict={dict.nav} />
            {children} <Footer locale={locale} />
        </>
    );
}
