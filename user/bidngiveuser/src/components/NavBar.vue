<script setup>
import { useRouter} from 'vue-router';

const router = useRouter();
</script>
<template>
    <section style="position: fixed;bottom: 0;width: 100vw">
        <nav style="display: flex; justify-content: space-evenly; align-items: center; background-color: #fff; padding: 15px 0px; color: white; font-family: Arial, sans-serif; font-size: 1em;">
            <a href="#home" @click.prevent="router.push('/dashboard')" style="text-decoration: none; color: #000; display: flex; flex-direction: column; align-items: center;">
                <span style="font-size: 1.5em;"><img src="/icons/home.svg" alt="Home icon" style="width: 1.3em;height: 1.3em;"></span>
                <span>Home</span>
            </a>
            <a href="#bids" @click.prevent="router.push('/bid')" style="text-decoration: none; color: #000; display: flex; flex-direction: column; align-items: center;">
                <span style="font-size: 1.5em;"><img src="/icons/moneybagnav.svg" alt="Home icon" style="width: 1.3em;height: 1.3em;"></span>
                <span>Bids</span>
            </a>
            <a href="#withdrawals" @click.prevent="router.push('/withdraw')" style="text-decoration: none; color: #000; display: flex; flex-direction: column; align-items: center;">
                <span style="font-size: 1.5em;"><img src="/icons/withdraw.svg" alt="Home icon" style="width: 1.3em;height: 1.3em;"></span>
                <span>Withdrawals</span>
            </a>
            <a href="#auction" @click.prevent="router.push('/merge-info')" style="text-decoration: none; color: #000; display: flex; flex-direction: column; align-items: center;">
                <span style="font-size: 1.5em;"><img src="/icons/auction.svg" alt="Home icon" style="width: 1.3em;height: 1.3em;"></span>
                <span>Merge</span>
            </a>
            <a href="#profile" @click.prevent="router.push('/profile')" style="text-decoration: none; color: #000; display: flex; flex-direction: column; align-items: center;">
                <span style="font-size: 1.5em;"><img src="/icons/profile.svg" alt="Home icon" style="width: 1.3em;height: 1.3em;"></span>
                <span>Profile</span>
            </a>
        </nav>
    </section>
</template>