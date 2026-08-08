interface ExperienceCardProps {
    period: string;
    role: string;
    organization: string;
    description: string;
    tags: string[];
}

export default function ExperienceCard({
    period,
    role,
    organization,
    description,
    tags,
}: ExperienceCardProps) {
    return (
        <div className="rounded-3xl border border-[#E7E2DA] bg-[#F8F7F4] p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_18px_40px_rgba(31,41,55,0.06)]">
            <p className="text-sm font-semibold text-[#C56E3D]">{period}</p>

            <h3 className="mt-3 text-2xl font-semibold text-[#1F2937]">
                {role}
            </h3>

            <p className="text-lg font-medium text-[#374151]">
                {organization}
            </p>

            <p className="mt-4 text-base leading-relaxed text-[#6B7280]">
                {description}
            </p>

            <div className="mt-5 flex flex-wrap gap-2">
                {tags.map((tag) => (
                    <span
                        key={tag}
                        className="rounded-full border border-[#E7E2DA] bg-white px-3 py-1 text-xs font-medium text-[#1F2937]"
                    >
                        {tag}
                    </span>
                ))}
            </div>
        </div>
    );
}