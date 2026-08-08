import Link from 'next/link';
import { ArrowRight } from 'lucide-react';
import Container from '@/components/common/Container';
import FadeInSection from '@/components/common/FadeInSection';

interface HeroSectionProps {
    locale: string;
    dict: {
        badge: string;
        title: string;
        description: string;
        primaryButton: string;
        secondaryButton: string;
    };
}

export default function HeroSection({
    locale,
    dict,
}: HeroSectionProps) {
    return (
        <section className="bg-[#F8F7F4] py-20 md:py-28">
            <FadeInSection>
                <Container>
                    <div className="max-w-4xl">
                        <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#C56E3D]">
                            {dict.badge}
                        </p>

                        <h1 className="mt-6 whitespace-pre-line text-5xl font-bold leading-[1.02] tracking-tight text-[#1F2937] md:text-7xl">
                            {dict.title}
                        </h1>

                        <p className="mt-8 max-w-2xl text-lg leading-relaxed text-[#6B7280] md:text-xl">
                            {dict.description}
                        </p>

                        <div className="mt-10 flex flex-wrap gap-4">
                            <Link
                                href={`/${locale}#projects`}
                                className="inline-flex items-center gap-2 rounded-full bg-[#1F2937] px-6 py-3 text-sm font-medium text-white transition hover:bg-[#111827]"
                            >
                                {dict.primaryButton}
                                <ArrowRight size={18} />
                            </Link>

                            <Link
                                href={`/${locale}#contact`}
                                className="inline-flex items-center rounded-full border border-[#1F2937] px-6 py-3 text-sm font-medium text-[#1F2937] transition hover:bg-[#1F2937] hover:text-white"
                            >
                                {dict.secondaryButton}
                            </Link>
                        </div>
                    </div>
                </Container>
            </FadeInSection>
        </section>
    );
}
