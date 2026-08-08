import Link from 'next/link';

interface ProjectCardProps {
    title: string;
    description: string;
    tags: string[] | string;
    time?: string;
    type?: string;
    slug: string;
    image_url?: string | null;
    locale: string;
}
export default function ProjectCard({
    title,
    description,
    tags,
    time,
    type,
    slug,
    image_url,
    locale,
}: ProjectCardProps) {
    const tagList = Array.isArray(tags)
        ? tags
        : String(tags)
            .replace(/[{}"]/g, '')
            .split(',')
            .map((tag) => tag.trim())
            .filter(Boolean);

    return (
        <Link
            href={`/${locale}/projects/${slug}`}
            className="group block rounded-3xl border border-[#E7E2DA] bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:border-[#C56E3D] hover:shadow-[0_18px_40px_rgba(31,41,55,0.08)]"
        >
            {image_url ? (
                <img
                    src={image_url}
                    alt={title}
                    className="mb-6 h-44 w-full rounded-2xl object-cover"
                />
            ) : (
                <div className="mb-6 h-44 w-full rounded-2xl bg-[#F3F1EC]" />
            )}

            {(time || type) && (
                <div className="flex items-center justify-between text-sm text-[#6B7280]">
                    <span>{time}</span>
                    {type && (
                        <span className="rounded-full border border-[#E7E2DA] px-3 py-1 text-xs font-medium text-[#1F2937]">
                            {type}
                        </span>
                    )}
                </div>
            )}

            <h3 className="mt-4 text-2xl font-semibold text-[#1F2937] group-hover:text-[#C56E3D] transition-colors">
                {title}
            </h3>

            <p className="mt-3 text-base leading-relaxed text-[#6B7280]">
                {description}
            </p>

            <div className="mt-6 flex flex-wrap gap-2">
                {tagList.map((tag) => (
                    <span
                        key={tag}
                        className="rounded-full border border-[#E7E2DA] bg-[#F8F7F4] px-3 py-1 text-xs font-medium text-[#1F2937]"
                    >
                        {tag}
                    </span>
                ))}
            </div>

            <p className="mt-6 text-sm font-medium text-[#C56E3D]">
                View Details →
            </p>
        </Link>
    );
}