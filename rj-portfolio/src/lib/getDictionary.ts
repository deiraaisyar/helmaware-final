import en from '@/messages/en';
import id from '@/messages/id';

export async function getDictionary(locale: string) {
    return locale === 'id' ? id : en;
}